import json

from river import compose, datasets, facto, metrics, optim, preprocessing
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


# feature engineering
# 1. categorical values
def split_genres(x):
    genres = x["genres"].split(", ")
    return {f"genre_{genre}": 1 / len(genres) for genre in genres}


# 2. Numerical variables
def bin_age(x):
    if x["age"] <= 18:
        return {"age_0-18": 1}
    elif x["age"] <= 32:
        return {"age_19-32": 1}
    elif x["age"] < 55:
        return {"age_33-54": 1}
    else:
        return {"age_55-100": 1}


def debug_ffm():
    ffm_params = {
        "n_factors": 10,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor += (
        compose.Select("genres")
        | compose.FuncTransformer(split_genres)
        | compose.Prefixer("item_")
    )
    regressor += (
        compose.Select("age")
        | compose.FuncTransformer(bin_age)
        | compose.Prefixer("user_")
    )
    regressor += compose.Select("gender") | compose.Prefixer("user_")
    regressor |= facto.FFMRegressor(**ffm_params)

    print(regressor)
    evaluate(regressor, False)
    debug(regressor)


def main():
    debug_ffm()


main()
