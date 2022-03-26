import os
import json
import tensorflow as tf

from coordinator import (
    start_coordinator_create_per_worker_dataset,
    start_coordinator_fetch,
)



flags = tf.compat.v1.flags
flags.DEFINE_string("task_type", "worker", "Either worker or ps")
flags.DEFINE_integer("task_index", 0, "task index e.g. 0")
flags.DEFINE_integer("coordinator_type", 0, "coordinator type e.g. 0")
FLAGS = flags.FLAGS

task = {"type": FLAGS.task_type, "index": FLAGS.task_index}
print(task)

os.environ["TF_CONFIG"] = json.dumps(
    {
        "cluster": {
            "worker": ["localhost:3000"],
            "ps": ["localhost:3001", "localhost:3002"],
            "chief": ["localhost:3003"],
        },
        "task": task,
    }
)


cluster_resolver = tf.distribute.cluster_resolver.TFConfigClusterResolver()

# Set the environment variable to allow reporting worker and ps failure to the
# coordinator. This is a workaround and won't be necessary in the future.
def start_tensorflow_server():
    os.environ["GRPC_FAIL_FAST"] = "use_caller"

    server = tf.distribute.Server(
        cluster_resolver.cluster_spec(),
        job_name=cluster_resolver.task_type,
        task_index=cluster_resolver.task_id,
        protocol=cluster_resolver.rpc_layer or "grpc",
        start=True,
    )
    server.join()


def start_evaluator():
    print('evaluator')


def start_coordinator(coordinator_type):
    strategy = tf.distribute.experimental.ParameterServerStrategy(
        cluster_resolver=cluster_resolver
    )
    coordinator = tf.distribute.experimental.coordinator.ClusterCoordinator(
        strategy=strategy
    )

    if coordinator_type == 0:
        start_coordinator_create_per_worker_dataset(strategy, coordinator)
    elif coordinator_type == 1:
        start_coordinator_fetch(strategy, coordinator)
    elif coordinator_type == 2:
        start_training_with_keras(strategy)


def start_training_with_keras(strategy):
    '''keras.models internally create ClusterCoordinator
    1. Create keras DatasetCreator with dataset_fn.
    2. Build a model in strategy.scope()
    3. Fit the model with callbacks.
    '''
    def dataset_fn(input_context):
        global_batch_size = 64
        batch_size = input_context.get_per_replica_batch_size(global_batch_size)

        x = tf.random.uniform((10, 10))
        y = tf.random.uniform((10,))

        dataset = tf.data.Dataset.from_tensor_slices((x, y)).shuffle(10).repeat()
        dataset = dataset.shard(
            input_context.num_input_pipelines, input_context.input_pipeline_id
        )
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(2)

        return dataset


    dc = tf.keras.utils.experimental.DatasetCreator(dataset_fn)

    with strategy.scope():
        model = tf.keras.models.Sequential([tf.keras.layers.Dense(10)])

        model.compile(tf.keras.optimizers.SGD(), loss="mse", steps_per_execution=10)

    working_dir = '/tmp/my_working_dir'
    log_dir = os.path.join(working_dir, 'log')
    ckpt_filepath = os.path.join(working_dir, 'ckpt')
    backup_dir = os.path.join(working_dir, 'backup')

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir=log_dir),
        tf.keras.callbacks.ModelCheckpoint(filepath=ckpt_filepath),
        tf.keras.callbacks.BackupAndRestore(backup_dir=backup_dir),
    ]

    model.fit(dc, epochs=5, steps_per_epoch=20, callbacks=callbacks)


def main():
    if cluster_resolver.task_type in ("worker", "ps"):
        # Start a TensorFlow server and wait.
        start_tensorflow_server()
    elif cluster_resolver.task_type == "evaluator":
        # Run side-car evaluation
        start_evaluator()
    else:
        # Run the coordinator.
        print(f"start coordinator {FLAGS.coordinator_type}")
        start_coordinator(FLAGS.coordinator_type)


if __name__ == '__main__':
    main()
