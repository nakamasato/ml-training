import tensorflow as tf


def dataset_from_rannge():
    dataset = tf.data.Dataset.range(100)
    def dataset_fn(ds):
        return ds.filter(lambda x: x < 5)


    dataset = dataset.apply(dataset_fn)
    print(list(dataset.as_numpy_iterator()))


def _gen():
    i = 0
    while True:
        i += 1
        yield f"msg-{i}"


def dataset_from_generator():
    dataset = tf.data.Dataset.from_generator(_gen, output_signature=tf.TensorSpec(shape=(), dtype=tf.string))
    iterator = iter(dataset)
    optional = iterator.get_next_as_optional()
    print(optional.has_value())
    print(optional.get_value())


def dataset_from_tfds():
    import tensorflow_datasets as tfds
    ratings = tfds.load("movielens/100k-ratings", split="train")
    # each example: key:str -> tf.Tensor
    ratings = ratings.map(lambda x: {
        "movie_title": x["movie_title"],
        "user_id": x["user_id"]
    })


    iterator = iter(ratings)
    rating = iterator.get_next()
    print(rating)
    # {'movie_title': <tf.Tensor: shape=(), dtype=string, numpy=b"One Flew Over the Cuckoo's Nest (1975)">,
    # 'user_id': <tf.Tensor: shape=(), dtype=string, numpy=b'138'>}


def main():
    dataset_from_rannge()
    dataset_from_generator()
    dataset_from_tfds()


if __name__ == "__main__":
    main()
