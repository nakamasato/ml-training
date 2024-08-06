import tensorflow as tf

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



dataset = tf.data.Dataset.from_generator(_gen, output_signature=tf.TensorSpec(shape=(), dtype=tf.string))
iterator = iter(dataset)
optional = iterator.get_next_as_optional()
print(optional.has_value())
print(optional.get_value())
