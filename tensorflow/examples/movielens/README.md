# [Datalens](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

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
