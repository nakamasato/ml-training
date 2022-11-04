import json

from river import compose, datasets, facto, metrics, optim, preprocessing, reco, stats
from river.evaluate import progressive_val_score

for x, y in datasets.MovieLens100K():
    print(f"x = {json.dumps(x, indent=4)}\ny = {y}")
    break


def evaluate(model, unpack_user_and_item=True):
    X_y = datasets.MovieLens100K(unpack_user_and_item)
    metric = metrics.MAE() + metrics.RMSE()
    _ = progressive_val_score(
        X_y, model, metric, print_every=25_000, show_time=True, show_memory=True
    )


def debug(model):
    for x, _ in datasets.MovieLens100K():
        report = model.debug_one(x)
        print(report)
        break


def biased_mf(run=False):
    # Biased Matrix Factorization
    print("---- Biased Matrix Factorization ----")
    if not run:
        print("[100,000] MAE: 0.748559, RMSE: 0.947854 – 0:00:07.202234 – 1.69 MB")
        return
    biased_mf_params = {
        "n_factors": 10,
        "bias_optimizer": optim.SGD(0.025),
        "latent_optimizer": optim.SGD(0.05),
        "weight_initializer": optim.initializers.Zeros(),
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.1, seed=73),
        "l2_bias": 0.0,
        "l2_latent": 0.0,
    }

    model = preprocessing.PredClipper(
        regressor=reco.BiasedMF(**biased_mf_params), y_min=1, y_max=5
    )

    evaluate(model)


def main():
    biased_mf(True)


main()
