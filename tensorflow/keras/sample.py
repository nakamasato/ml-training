import tensorflow as tf


# 1. With the "Functional API",
inputs = tf.keras.Input(shape=(None, None, 3))
processed = tf.keras.layers.RandomCrop(width=32, height=32)(inputs)
conv = tf.keras.layers.Conv2D(filters=2, kernel_size=3)(processed)
pooling = tf.keras.layers.GlobalAveragePooling2D()(conv)
feature = tf.keras.layers.Dense(10)(pooling)

full_model = tf.keras.Model(inputs, feature)
backbone = tf.keras.Model(processed, conv)
activations = tf.keras.Model(conv, feature)


# 2. By subclassing the Model class
class MyModel(tf.keras.Model):

    def __init__(self) -> None:
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(4, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(5, activation=tf.nn.softmax)
        self.dropout = tf.keras.layers.Dropout(0.5)

    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        if training:
            x = self.dropout(x, training=training)
        return self.dense2(x)

model = MyModel()
model.compile()
# model.fit(x, y)
# model.predict(x)


inputs = tf.keras.Input(shape=(784,), name="digits")
x = tf.keras.layers.Dense(64, activation="relu", name="dense_1")(inputs)
x = tf.keras.layers.Dense(64, activation="relu", name="dense_2")(x)
outputs = tf.keras.layers.Dense(10, activation="softmax", name="predictions")(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)


## Data Preparation
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Preprocess the data (these are NumPy arrays)
x_train = x_train.reshape(60000, 784).astype("float32") / 255
x_test = x_test.reshape(10000, 784).astype("float32") / 255

y_train = y_train.astype("float32")
y_test = y_test.astype("float32")

# Reserve 10,000 samples for validation
x_val = x_train[-10000:]
y_val = y_train[-10000:]
x_train = x_train[:-10000]
y_train = y_train[:-10000]


model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),  # Optimizer
    # Loss function to minimize
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)


print("Fit model on training data")
history = model.fit(
    x_train,
    y_train,
    batch_size=64,
    epochs=2,
    # We pass some validation for
    # monitoring validation loss and metrics
    # at the end of each epoch
    validation_data=(x_val, y_val),
)

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(x_test, y_test, batch_size=128)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for 3 samples")
predictions = model.predict(x_test[:3])
print("predictions shape:", predictions.shape)
