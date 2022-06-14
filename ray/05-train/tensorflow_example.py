import json
import os
import sys

import numpy as np
import tensorflow as tf
from ray import train
from ray.train import Trainer

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ.pop('TF_CONFIG', None)

if '.' not in sys.path:
    sys.path.insert(0, '.')


def mnist_dataset(batch_size):
    (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
    # The `x` arrays are in uint8 and have values in the [0, 255] range.
    # You need to convert them to float32 with values in the [0, 1] range.
    x_train = x_train / np.float32(255)
    y_train = y_train.astype(np.int64)
    train_dataset = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)).shuffle(60000).repeat().batch(batch_size)
    return train_dataset


def build_and_compile_cnn_model():
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
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
        metrics=['accuracy'])
    return model


def train_func():

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

    multi_worker_dataset = mnist_dataset(global_batch_size)

    with strategy.scope():
        multi_worker_model = build_and_compile_cnn_model()

    multi_worker_model.fit(multi_worker_dataset, epochs=3, steps_per_epoch=70)


per_worker_batch_size = 64
global_batch_size = per_worker_batch_size * train.world_size()

trainer = Trainer(backend="tensorflow", num_workers=2)

trainer.start()  # set up resources
trainer.run(train_func)
trainer.shutdown()  # clean up resources
