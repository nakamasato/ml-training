import tensorflow as tf


def func_basic():
    v = tf.Variable(1)

    @tf.function
    def f(x):
        for i in tf.range(x):
            v.assign_add(i)

    f(3)
    print(v)


def normal_variable():
    data = [1, 2, 3, 4, 5]

    def dataset_fn():
        return tf.data.Dataset.from_tensor_slices(data)

    v = tf.Variable(initial_value=0)

    print(v.read_value())
    @tf.function
    def worker_fn(iterator):
        v.assign_add(next(iterator))
        return v.read_value()

    iterator = iter(dataset_fn())
    for _ in range(len(data)):
        worker_fn(iterator)

    print(f"{v=}")
    print(f"{v.read_value()}")
    assert v.read_value() == sum(data)

normal_variable()
