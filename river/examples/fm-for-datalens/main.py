import argparse
import json

from river import compose, datasets, facto, metrics, optim, preprocessing, reco, stats
from river.evaluate import progressive_val_score

for x, y in datasets.MovieLens100K(False):
    print(f"x = {json.dumps(x, indent=4)}\ny = {y}")
    break


for x, y, d in datasets.MovieLens100K(True):
    print(f"{x=}\n{y=}\n{d=}")
    break


def evaluate(model, unpack_user_and_item=False):
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


def naive_prediction(run=False):
    # Naive prediction (Mean)
    print("---- Naive prediction (Mean) ----")
    if not run:
        print("MAE: 0.942162, RMSE: 1.125783")
        return
    mean = stats.Mean()
    metric = metrics.MAE() + metrics.RMSE()

    for i, x_y in enumerate(datasets.MovieLens100K(), start=1):
        _, y = x_y
        metric.update(y, mean.get())
        mean.update(y)

        if not i % 25_000:
            print(f"[{i:,d}] {metric}")


def linear_regression(run=False):
    # Baseline Model (linear regression)
    print("---- Baseline Model ----")
    if not run:
        print("[100,000] MAE: 0.754651, RMSE: 0.954148 – 0:00:03.573886 – 306.03 KB")
        return
    baseline_params = {
        "optimizer": optim.SGD(0.025),
        "l2": 0.0,
        "initializer": optim.initializers.Zeros(),
    }

    model = preprocessing.PredClipper(
        regressor=reco.Baseline(**baseline_params), y_min=1, y_max=5
    )

    evaluate(model, True)


def funk_mf(run=False):
    # Funk MF
    # pure form of matrix factorization consisting of only learning the users and items latent representations
    print("---- Funk Matrix Factorization ----")
    if not run:
        print("[100,000] MAE: 0.944883, RMSE: 1.227688 – 0:00:06.424226 – 1.5 MB")
        return
    funk_mf_params = {
        "n_factors": 10,
        "optimizer": optim.SGD(0.05),
        "l2": 0.1,
        "initializer": optim.initializers.Normal(mu=0.0, sigma=0.1, seed=73),
    }

    model = preprocessing.PredClipper(
        regressor=reco.FunkMF(**funk_mf_params), y_min=1, y_max=5
    )

    evaluate(model, True)


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

    evaluate(model, True)


def mimic_biased_mf(run=False):
    # Mimic Biased Matrix Factorization
    # mimic reco.BiasedMF with reco.FMRegressor
    print("---- Mimic Biased Matrix Factorization ----")
    if not run:
        print("[100,000] MAE: 0.748609, RMSE: 0.947994 – 0:00:15.836149 – 1.77 MB")
        return
    fm_params = {
        "n_factors": 10,
        "weight_optimizer": optim.SGD(0.025),
        "latent_optimizer": optim.SGD(0.05),
        "sample_normalization": False,
        "l1_weight": 0.0,
        "l2_weight": 0.0,
        "l1_latent": 0.0,
        "l2_latent": 0.0,
        "intercept": 3,
        "intercept_lr": 0.01,
        "weight_initializer": optim.initializers.Zeros(),
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.1, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor |= facto.FMRegressor(**fm_params)

    model = preprocessing.PredClipper(regressor=regressor, y_min=1, y_max=5)

    evaluate(model, False)
    print(regressor)


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


def mf_with_improved_feature(run=False):
    print("---- Matrix Factorization with improved features ----")
    if not run:
        print("[100,000] MAE: 0.749994, RMSE: 0.951435 – 0:00:39.099781 – 2.2 MB")
        return
    fm_params = {
        "n_factors": 14,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor += compose.Select("genres") | compose.FuncTransformer(split_genres)
    regressor += compose.Select("age") | compose.FuncTransformer(bin_age)
    regressor |= facto.FMRegressor(**fm_params)

    model = preprocessing.PredClipper(regressor=regressor, y_min=1, y_max=5)

    evaluate(model)


# Higher-Order Factorization Machines (HOFM)
def high_order_fm(run=False):
    print("---- Higher-Order Factorization Machines (HOFM) ----")
    if not run:
        print("[100,000] MAE: 0.750607, RMSE: 0.951982 – 0:03:19.012759 – 4.07 MB")
        return
    hofm_params = {
        "degree": 3,
        "n_factors": 12,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor += compose.Select("genres") | compose.FuncTransformer(split_genres)
    regressor += compose.Select("age") | compose.FuncTransformer(bin_age)
    regressor |= facto.HOFMRegressor(**hofm_params)

    model = preprocessing.PredClipper(regressor=regressor, y_min=1, y_max=5)

    evaluate(model)


# Field-aware Factorization Machines (FFM)
def ffm(run=False):
    print("---- Field-aware Factorization Machines (FFM) ----")
    if not run:
        print("[100,000] MAE: 0.749542, RMSE: 0.949769 – 0:00:59.588101 – 4.75 MB")
        return
    ffm_params = {
        "n_factors": 8,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor += compose.Select("genres") | compose.FuncTransformer(split_genres)
    regressor += compose.Select("age") | compose.FuncTransformer(bin_age)
    regressor |= facto.FFMRegressor(**ffm_params)

    model = preprocessing.PredClipper(regressor=regressor, y_min=1, y_max=5)

    evaluate(model)


# Field-weighted Factorization Machines (FwFM)
def fwfm(run=False):
    print("---- Field-weighted Factorization Machines (FwFM) ----")
    if not run:
        print("100,000] MAE: 0.755697, RMSE: 0.956542 – 0:01:14.461360 – 1.79 MB")
        return
    fwfm_params = {
        "n_factors": 10,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "seed": 73,
    }

    regressor = compose.Select("user", "item")
    regressor += compose.Select("genres") | compose.FuncTransformer(split_genres)
    regressor += compose.Select("age") | compose.FuncTransformer(bin_age)
    regressor |= facto.FwFMRegressor(**fwfm_params)

    model = preprocessing.PredClipper(regressor=regressor, y_min=1, y_max=5)

    evaluate(model)


def ffm_with_n(n, run=False):
    print(f"---- Field-aware Factorization Machines (FFM) with {n}_factor ----")
    if not run:
        return
    ffm_params = {
        "n_factors": n,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor += compose.Select("genres") | compose.FuncTransformer(split_genres)
    regressor += compose.Select("age") | compose.FuncTransformer(bin_age)
    regressor |= facto.FFMRegressor(**ffm_params)

    model = preprocessing.PredClipper(regressor=regressor, y_min=1, y_max=5)

    evaluate(model, False)


def debug_fm():
    fm_params = {
        "n_factors": 10,
        "weight_optimizer": optim.SGD(0.025),
        "latent_optimizer": optim.SGD(0.05),
        "sample_normalization": False,
        "l1_weight": 0.0,
        "l2_weight": 0.0,
        "l1_latent": 0.0,
        "l2_latent": 0.0,
        "intercept": 3,
        "intercept_lr": 0.01,
        "weight_initializer": optim.initializers.Zeros(),
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.1, seed=73),
    }

    regressor = compose.Select("user", "item")
    regressor += compose.Select("genres") | compose.FuncTransformer(split_genres)
    regressor += compose.Select("age") | compose.FuncTransformer(bin_age)
    regressor |= facto.FMRegressor(**fm_params)
    evaluate(regressor, True)
    debug(regressor)


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


def main(
    run_naive_prediction=False,
    run_linear_regression=False,
    run_funk_mf=False,
    run_biased_mf=False,
    run_mimic_biased_mf=False,
    run_mf_with_improved_feature=False,
    run_high_order_fm=False,
    run_ffm=False,
    run_ffm_with_n=False,
    run_fwfm=False,
    run_all=False
):
    naive_prediction(run_naive_prediction or run_all)
    linear_regression(run_linear_regression or run_all)
    funk_mf(run_funk_mf or run_all)
    biased_mf(run_biased_mf or run_all)
    mimic_biased_mf(run_mimic_biased_mf or run_all)
    mf_with_improved_feature(run_mf_with_improved_feature or run_all)
    high_order_fm(run_high_order_fm or run_all)
    ffm(run_ffm or run_all)
    fwfm(run_fwfm or run_all)
    for n in range(2, 20, 3):
        ffm_with_n(n, run_ffm_with_n or run_all)
    if run_ffm or run_all:
        debug_ffm()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="FM for datalens",
        description="river example with FM for datalens data",
    )
    parser.add_argument(
        "--native-prediction",
        help="Execute native_prediction",
        action="store_true",
    )
    parser.add_argument(
        "--linear-regression",
        help="Execute linear_regression",
        action="store_true",
    )
    parser.add_argument(
        "--funk-mf",
        help="Execute funk_mf",
        action="store_true",
    )
    parser.add_argument(
        "--biased-mf",
        help="Execute biased_mf",
        action="store_true",
    )
    parser.add_argument(
        "--mimic-biased-mf",
        help="Execute mimic_biased_mf",
        action="store_true",
    )
    parser.add_argument(
        "--mf-with-improved-feature",
        help="Execute mf_with_improved_feature",
        action="store_true",
    )
    parser.add_argument(
        "--high-order-fm",
        help="Execute high_order_fm",
        action="store_true",
    )
    parser.add_argument(
        "--ffm",
        help="Execute ffm",
        action="store_true",
    )
    parser.add_argument(
        "--ffm-with-n",
        help="Execute ffm with different n",
        action="store_true",
    )
    parser.add_argument(
        "--fwfm",
        help="Execute fwfm",
        action="store_true",
    )
    parser.add_argument(
        "--all",
        help="Execute all",
        action="store_true",
    )
    args = parser.parse_args()
    main(
        args.native_prediction,
        args.linear_regression,
        args.funk_mf,
        args.biased_mf,
        args.mimic_biased_mf,
        args.mf_with_improved_feature,
        args.high_order_fm,
        args.ffm,
        args.ffm_with_n,
        args.fwfm,
        args.all,
    )
