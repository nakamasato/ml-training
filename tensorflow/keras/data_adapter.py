import numpy as np
import tensorflow as tf

from keras.engine import data_adapter


def mnist_dataset(batch_size):
    (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
    # The `x` arrays are in uint8 and have values in the [0, 255] range.
    # You need to convert them to float32 with values in the [0, 1] range.
    x_train = x_train / np.float32(255)
    y_train = y_train.astype(np.int64)
    train_dataset = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)).shuffle(60000).repeat().batch(batch_size)
    return train_dataset


def fit(
    x=None,
    y=None,
    batch_size=None,
    epochs=1,
    verbose='auto',
    callbacks=None,
    validation_split=0.,
    validation_data=None,
    shuffle=True,
    class_weight=None,
    sample_weight=None,
    initial_epoch=0,
    steps_per_epoch=None,
    validation_steps=None,
    validation_batch_size=None,
    validation_freq=1,
    max_queue_size=10,
    workers=1,
    use_multiprocessing=False
):
    steps_per_execution = 70
    _steps_per_execution = tf.Variable(
        steps_per_execution,
        dtype='int64',
        aggregation=tf.VariableAggregation.ONLY_FIRST_REPLICA)

    data_handler = data_adapter.get_data_handler(
        x=x,
        y=y,
        sample_weight=sample_weight,
        batch_size=batch_size,
        steps_per_epoch=steps_per_epoch,
        initial_epoch=initial_epoch,
        epochs=epochs,
        shuffle=shuffle,
        class_weight=class_weight,
        max_queue_size=max_queue_size,
        workers=workers,
        use_multiprocessing=use_multiprocessing,
        model=None,  # if use cluster coordinator need to pass.
        steps_per_execution=_steps_per_execution)

    for epoch, iterator in data_handler.enumerate_epochs():
        print(f"epoch {epoch}")
        with data_handler.catch_stop_iteration():
            for step in data_handler.steps():
                tmp_logs = train_function(iterator)
                print(tmp_logs)


def train_function(iter):
    data = next(iter)
    outputs = run_step(data)
    return outputs


def run_step(data):
    outputs = train_step(data)
    return outputs


def train_step(data):
    x, y, sample_weight = data_adapter.unpack_x_y_sample_weight(data)
    print(f"x: {tf.shape(x)}, y: {tf.shape(y)}, {sample_weight=}")
    return {'loss': 1, 'accuracy': 0}


def main():
    per_worker_batch_size = 16
    num_workers = 2
    global_batch_size = per_worker_batch_size * num_workers
    multi_worker_dataset = mnist_dataset(global_batch_size)
    fit(multi_worker_dataset, epochs=2, steps_per_epoch=70)


if __name__ == '__main__':
    main()
