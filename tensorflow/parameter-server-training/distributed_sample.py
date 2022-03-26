import tensorflow as tf
from train_in_process_cluster import create_in_process_cluster


def distributed():
    # Create Cluster
    cluster_resolver = create_in_process_cluster(num_workers=3, num_ps=2)

    # Init strategy
    strategy = tf.distribute.experimental.ParameterServerStrategy(
        cluster_resolver
    )

    # Init coordinator
    coordinator = tf.distribute.experimental.coordinator.ClusterCoordinator(
        strategy=strategy
    )

    data = [1, 2, 3, 4, 5]

    def dataset_fn():
        return tf.data.Dataset.from_tensor_slices(data)

    # create variable in strategy.scope()
    with strategy.scope():
        v = tf.Variable(initial_value=0) # variable will be created on PS.

    print(v.read_value())
    @tf.function
    def worker_fn(iterator):
        v.assign_add(next(iterator))
        return v.read_value()

    iterator = iter(dataset_fn())
    for _ in range(len(data)):
        result = coordinator.schedule(worker_fn, args=(iterator,))
    print(coordinator.fetch(result))
    print(f"{v=}, {v.device=}")
    print(f"{v.read_value()}")
    assert v.read_value() == sum(data)


distributed()
