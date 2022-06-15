import json
import os

import numpy as np
import ray
import tensorflow as tf
from ray import train
from ray.train import Trainer
from tensorflow.keras.callbacks import Callback


class TrainReportCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        train.report(**logs)


def mnist_dataset(batch_size):
    (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
    # The `x` arrays are in uint8 and have values in the [0, 255] range.
    # You need to convert them to float32 with values in the [0, 1] range.
    x_train = x_train / np.float32(255)
    y_train = y_train.astype(np.int64)
    train_dataset = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)).shuffle(60000).repeat().batch(batch_size)
    return train_dataset


def build_and_compile_cnn_model(config):
    learning_rate = config.get("lr", 0.001)
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(28, 28)),
        tf.keras.layers.Reshape(target_shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
        metrics=['accuracy'])
    return model


def train_func(config):

    per_worker_batch_size = config.get("batch_size", 64)
    epochs = config.get("epochs", 3)
    steps_per_epoch = config.get("steps_per_epoch", 70)

    tf_config = json.loads(os.environ["TF_CONFIG"])
    num_workers = len(tf_config["cluster"]["worker"])

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

    global_batch_size = per_worker_batch_size * num_workers
    multi_worker_dataset = mnist_dataset(global_batch_size)

    with strategy.scope():
        multi_worker_model = build_and_compile_cnn_model(config)

    history = multi_worker_model.fit(
        multi_worker_dataset,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch,
        callbacks=[TrainReportCallback()],
    )
    results = history.history
    return results


def train_tensorflow_mnist(num_workers=2, use_gpu=False, epochs=4):
    trainer = Trainer(backend="tensorflow", num_workers=num_workers, use_gpu=use_gpu)

    trainer.start()  # set up resources
    results = trainer.run(
        train_func=train_func,
        config={"lr": 1e-3, "batch_size": 64, "epochs": epochs}
    )
    trainer.shutdown()  # clean up resources
    print(f"Results: {results[0]}")


# ray.init(address='auto') # on cluster
train_tensorflow_mnist()
