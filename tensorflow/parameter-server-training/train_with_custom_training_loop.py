import os
import random
import tensorflow as tf
from train_in_process_cluster import create_in_process_cluster


# Set the environment variable to allow reporting worker and ps failure to the
# coordinator. This is a workaround and won't be necessary in the future.
os.environ["GRPC_FAIL_FAST"] = "use_caller"

NUM_WORKERS = 3
NUM_PS = 2
cluster_resolver = create_in_process_cluster(NUM_WORKERS, NUM_PS)
tf.debugging.set_log_device_placement(True)

# Instantiate a ParameterServerStrategy
variable_partitioner = tf.distribute.experimental.partitioners.MinSizePartitioner(
    min_shard_bytes=(256 << 10), max_shards=NUM_PS
)

strategy = tf.distribute.experimental.ParameterServerStrategy(
    cluster_resolver, variable_partitioner=variable_partitioner
)

# Set up data https://www.tensorflow.org/tutorials/distribute/parameter_server_training#set_up_the_data

feature_vocab = [
    "avenger",
    "ironman",
    "batman",
    "hulk",
    "spiderman",
    "kingkong",
    "wonder_woman",
]
label_vocab = ["yes", "no"]

with strategy.scope():
    feature_lookup_layer = tf.keras.layers.StringLookup(
        vocabulary=feature_vocab, mask_token=None
    )
    label_lookup_layer = tf.keras.layers.StringLookup(
        vocabulary=label_vocab, num_oov_indices=0, mask_token=None
    )

    raw_feature_input = tf.keras.layers.Input(
        shape=(3,), dtype=tf.string, name="feature"
    )
    feature_id_input = feature_lookup_layer(raw_feature_input)
    feature_preprocess_stage = tf.keras.Model(
        {"features": raw_feature_input}, feature_id_input
    )

    raw_label_input = tf.keras.layers.Input(shape=(1,), dtype=tf.string, name="label")
    label_id_input = label_lookup_layer(raw_label_input)

    label_preprocess_stage = tf.keras.Model({"label": raw_label_input}, label_id_input)


def feature_and_label_gen(num_examples=200):
    examples = {"features": [], "label": []}
    for _ in range(num_examples):
        features = random.sample(feature_vocab, 3)
        label = ["yes"] if "avenger" in features else ["no"]
        examples["features"].append(features)
        examples["label"].append(label)
    return examples


examples = feature_and_label_gen()


def dataset_fn(_):
    raw_dataset = tf.data.Dataset.from_tensor_slices(examples)

    train_dataset = (
        raw_dataset.map(
            lambda x: (
                {"features": feature_preprocess_stage(x["features"])},
                label_preprocess_stage(x["label"]),
            )
        )
        .shuffle(200)
        .batch(32)
        .repeat()
    )
    return train_dataset


# Build the model https://www.tensorflow.org/tutorials/distribute/parameter_server_training#build_the_model
# These variables created under the `strategy.scope` will be placed on parameter
# servers in a round-robin fashion.
with strategy.scope():
    # Create the model. The input needs to be compatible with Keras processing layers.
    model_input = tf.keras.layers.Input(shape=(3,), dtype=tf.int64, name="model_input")

    emb_layer = tf.keras.layers.Embedding(
        input_dim=len(feature_lookup_layer.get_vocabulary()), output_dim=16384
    )
    emb_output = tf.reduce_mean(emb_layer(model_input), axis=1)
    dense_output = tf.keras.layers.Dense(units=1, activation="sigmoid")(emb_output)
    model = tf.keras.Model({"features": model_input}, dense_output)

    optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.1)
    accuracy = tf.keras.metrics.Accuracy()

assert len(emb_layer.weights) == 2
assert emb_layer.weights[0].shape == (4, 16384)
assert emb_layer.weights[1].shape == (4, 16384)
assert emb_layer.weights[0].device == "/job:ps/replica:0/task:0/device:CPU:0"
assert emb_layer.weights[1].device == "/job:ps/replica:0/task:1/device:CPU:0"


# Define the training step https://www.tensorflow.org/tutorials/distribute/parameter_server_training#define_the_training_step
@tf.function
def step_fn(iterator):
    def replica_fn(batch_data, labels):
        with tf.GradientTape() as tape:
            pred = model(batch_data, training=True)
            per_example_loss = tf.keras.losses.BinaryCrossentropy(
                reduction=tf.keras.losses.Reduction.NONE
            )(labels, pred)
            loss = tf.nn.compute_average_loss(per_example_loss)
            gradients = tape.gradient(loss, model.trainable_variables)

        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        actual_pred = tf.cast(tf.greater(pred, 0.5), tf.int64)
        accuracy.update_state(labels, actual_pred)
        return loss

    batch_data, labels = next(iterator)
    losses = strategy.run(replica_fn, args=(batch_data, labels))
    return strategy.reduce(tf.distribute.ReduceOp.SUM, losses, axis=None)


# Dispatch training steps to remote workers https://www.tensorflow.org/tutorials/distribute/parameter_server_training#dispatch_training_steps_to_remote_workers

coordinator = tf.distribute.experimental.coordinator.ClusterCoordinator(strategy)


@tf.function
def per_worker_dataset_fn():
    return strategy.distribute_datasets_from_function(dataset_fn)


per_worker_dataset = coordinator.create_per_worker_dataset(per_worker_dataset_fn)
per_worker_iterator = iter(per_worker_dataset)

num_epoches = 4
steps_per_epoch = 5
for i in range(num_epoches):
    accuracy.reset_states()
    for _ in range(steps_per_epoch):
        coordinator.schedule(step_fn, args=(per_worker_iterator,))
    # Wait at epoch boundaries.
    coordinator.join()
    print("Finished epoch %d, accuracy is %f." % (i, accuracy.result().numpy()))


loss = coordinator.schedule(step_fn, args=(per_worker_iterator,))
print("Final loss is %f" % loss.fetch())

# Evaluation
# Inline Evaluation
# Direct evaluation
eval_dataset = (
    tf.data.Dataset.from_tensor_slices(feature_and_label_gen(num_examples=16))
    .map(
        lambda x: (
            {"features": feature_preprocess_stage(x["features"])},
            label_preprocess_stage(x["label"]),
        )
    )
    .batch(8)
)

eval_accuracy = tf.keras.metrics.Accuracy()

for batch_data, labels in eval_dataset:
    pred = model(batch_data, training=False)
    actual_pred = tf.cast(tf.greater(pred, 0.5), tf.int64)
    eval_accuracy.update_state(labels, actual_pred)

print("Evaluation accuracy: %f" % eval_accuracy.result())

# Distributed evaluation

with strategy.scope():
    # Define the eval metric on parameter servers.
    eval_accuracy = tf.keras.metrics.Accuracy()


@tf.function
def eval_step(iterator):
    def replica_fn(batch_data, labels):
        pred = model(batch_data, training=False)
        actual_pred = tf.cast(tf.greater(pred, 0.5), tf.int64)
        eval_accuracy.update_state(labels, actual_pred)

    batch_data, labels = next(iterator)
    strategy.run(replica_fn, args=(batch_data, labels))


def eval_dataset_fn():
    return (
        tf.data.Dataset.from_tensor_slices(feature_and_label_gen(num_examples=16))
        .map(
            lambda x: (
                {"features": feature_preprocess_stage(x["features"])},
                label_preprocess_stage(x["label"]),
            )
        )
        .shuffle(16)
        .repeat()
        .batch(8)
    )


per_worker_eval_dataset = coordinator.create_per_worker_dataset(eval_dataset_fn)
per_worker_eval_iterator = iter(per_worker_eval_dataset)

eval_steps_per_epoch = 2
for _ in range(eval_steps_per_epoch):
    coordinator.schedule(eval_step, args=(per_worker_eval_iterator,))
coordinator.join()
print("Evaluation accuracy: %f" % eval_accuracy.result())

# Side-car evaluation todo https://www.tensorflow.org/tutorials/distribute/parameter_server_training#side-car_evaluation
