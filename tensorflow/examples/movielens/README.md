# [Movielens](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

## Version

- tensorflow: 2.17.0
- keras: 2.17.0 (`poetry add tf_keras --group tensorflow`)

## Run

### retrieve

`TF_USE_LEGACY_KERAS=1` is set in `.env` (This is necessary because https://github.com/tensorflow/recommenders/issues/712)

```
poetry run python tensorflow/examples/movielens/retrieve.py
```

### rank

train Rank model and save the model

```
WRAPT_DISABLE_EXTENSIONS=1 poetry run python tensorflow/examples/movielens/rank.py
```

## Data

### ratings

1. bucketized_user_age
1. movie_genres
1. movie_id
1. movie_title
1. raw_user_age
1. timestamp
1. user_gender
1. user_id
1. user_occupation_label
1. user_occupation_text
1. user_rating
1. user_zip_code

### movies

1. movie_genres
1. movie_id
1. movie_title


## Basic Model

1. user_id
1. movie_title

## Embedding

`StringLookup` だと未知のユーザに対して、適当な値を作れない

```py
>>> user_ids_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
>>> user_ids_vocabulary
<StringLookup name=string_lookup_1, built=False>
>>> user_ids_vocabulary.adapt(["uid1", "uid2"])
>>> user_ids_vocabulary
<StringLookup name=string_lookup_1, built=False>
>>> user_ids_vocabulary("uid1")
<tf.Tensor: shape=(), dtype=int64, numpy=2>
>>> user_ids_vocabulary("uid2")
<tf.Tensor: shape=(), dtype=int64, numpy=1>
>>> user_ids_vocabulary("uid3")
<tf.Tensor: shape=(), dtype=int64, numpy=0>
>>> user_ids_vocabulary("uid4")
<tf.Tensor: shape=(), dtype=int64, numpy=0>
>>> user_ids_vocabulary("uid5")
<tf.Tensor: shape=(), dtype=int64, numpy=0>
```

```py
user_model(tf.constant("uid2")) # embeddingを取得できる
```

## Errors

1. [ValueError: Cannot convert '('c', 'o', 'u', 'n', 't', 'e', 'r')' to a shape. Found invalid entry 'c' of type '<class 'str'>' tfrs.metrics.FactorizedTopK](https://github.com/tensorflow/recommenders/issues/712): to be resolved by https://github.com/tensorflow/recommenders/pull/717 or `TF_USE_LEGACY_KERAS=1` with `poetry add tf_keras --group tensorflow`

1. `ValueError: Only input tensors may be passed as positional arguments. The following argument value should be passed as a keyword argument: 42 (of type <class 'str'>)`
    ```diff
    - print(RankingModel()((["42"], ["One Flew Over the Cuckoo's Nest (1975)"])))
    + user_id_tensor = tf.convert_to_tensor(["42"])
    + movie_title_tensor = tf.convert_to_tensor(["One Flew Over the Cuckoo's Nest (1975)"])
    + print(RankingModel()((user_id_tensor, movie_title_tensor)))
    ```

1. `ValueError: TensorFlowTrainer.make_train_function.<locals>.one_step_on_data(data) should not modify its Python input arguments. Modifying a copy is allowed. The following parameter(s) were modified: data`
    `features` is modified with `pop`

    ```diff
    - labels = features.pop("user_rating")
    + copied_features = features.copy()
    + labels = copied_features.pop("user_rating")
    ```
1. `ValueError: could not convert string to float: 'M*A*S*H (1970)'`

    ```diff

      test_ratings[movie_title] = model({
    -     "user_id": np.array(["42"]),
    -     "movie_title": np.array([movie_title])
    +     "user_id": tf.convert_to_tensor(["42"]),
    +     "movie_title": tf.convert_to_tensor([movie_title])
      })
    ```
1. `TypeError: this __dict__ descriptor does not support '_DictWrapper' objects` in `tf.saved_model.save(model, "export")`
    This is Python 3.12 specific issue and workaround is `WRAPT_DISABLE_EXTENSIONS=1 poetry run python tensorflow/examples/movielens/rank.py`
    https://github.com/tensorflow/tensorflow/issues/63548
