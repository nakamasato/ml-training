import tensorflow as tf
import os
from train_in_process_cluster import create_in_process_cluster


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


def main():
    # Set the environment variable to allow reporting worker and ps failure to the
    # coordinator. This is a workaround and won't be necessary in the future.
    os.environ["GRPC_FAIL_FAST"] = "use_caller"

    NUM_WORKERS = 3
    NUM_PS = 2
    cluster_resolver = create_in_process_cluster(NUM_WORKERS, NUM_PS)

    # Instantiate a ParameterServerStrategy
    variable_partitioner = tf.distribute.experimental.partitioners.MinSizePartitioner(
        min_shard_bytes=(256 << 10), max_shards=NUM_PS
    )

    strategy = tf.distribute.ParameterServerStrategy(
        cluster_resolver, variable_partitioner=variable_partitioner
    )

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


if __name__ == '__main__':
    main()
