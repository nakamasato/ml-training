import functools
import json
from collections import defaultdict

import redis
from redis_collections import DefaultDict
from river import compose, datasets, facto, metrics, optim
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
        print(x)
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


def main():
    # redis
    conn = redis.StrictRedis(host="localhost", port=6379, db=0)

    # init latents with DefaultDict
    latent_initializer = optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73)
    random_latents = functools.partial(latent_initializer, shape=10)
    field_latents_dict = functools.partial(defaultdict, random_latents)
    latents = DefaultDict(field_latents_dict, key="ffm_latents", redis=conn)

    # init weights
    weight_initializer = optim.initializers.Zeros()
    weights = DefaultDict(weight_initializer, key="ffm_weights", redis=conn)

    ffm_params = {
        "n_factors": 10,
        "weight_optimizer": optim.SGD(0.01),
        "latent_optimizer": optim.SGD(0.025),
        "intercept": 3,
        "latents": latents,
        "weights": weights,
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
    print(
        f"intercept: {regressor.steps['FFMRegressor'].intercept}\n"
        f"weights (len): {len(regressor.steps['FFMRegressor'].weights)}\n"
        f"latents (len): {len(regressor.steps['FFMRegressor'].latents)}\n"
    )


main()
