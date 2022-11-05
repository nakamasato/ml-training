import functools
from collections import defaultdict

import redis
from flask import Flask, request
from redis_collections import DefaultDict
from river import compose, facto, optim


def create_app():

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    model = init_model_with_redis()

    @app.route("/", methods=["GET"])
    def predict():
        payload = request.json
        print(payload)
        print(model.debug_one(payload))
        res = model.predict_one(payload)
        return {"pred": res}

    return app


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


def init_model_with_redis():
    # TODO: Use common model for serving and training
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
        "latent_initializer": optim.initializers.Normal(mu=0.0, sigma=0.05, seed=73),
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
    return regressor
