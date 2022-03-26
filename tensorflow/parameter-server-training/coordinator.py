import tensorflow as tf
from random import randint
from train_in_process_cluster import create_in_process_cluster

NUM_WORKERS = 3
NUM_PS = 2


def main():
    cluster_resolver = create_in_process_cluster(NUM_WORKERS, NUM_PS)
    strategy = tf.distribute.experimental.ParameterServerStrategy(
        cluster_resolver
    )
    coordinator = tf.distribute.experimental.coordinator.ClusterCoordinator(
        strategy=strategy
    )
    start_coordinator_create_per_worker_dataset(strategy, coordinator)
    start_coordinator_fetch(strategy, coordinator)
    start_coordinator_update_variable(strategy, coordinator)
    distributed_variables(strategy)


def start_coordinator_create_per_worker_dataset(strategy, coordinator):
    '''Example of create_per_worker_dataset.
    https://www.tensorflow.org/api_docs/python/tf/distribute/experimental/coordinator/ClusterCoordinator#example
    1. Create dataset per worker.
        [
            <tf.Tensor: shape=(), dtype=int32, numpy=3>,
            <tf.Tensor: shape=(), dtype=int32, numpy=3>,
            <tf.Tensor: shape=(), dtype=int32, numpy=3>
        ]
    2. Call worker func for the iteration (per_worker_dataset)
    3. Remote value should be three.
    '''

    data = [randint(1, 100) for _ in range(10)]  # generate random data

    @tf.function
    def worker_fn(iterator):
        return next(iterator)

    def per_worker_dataset_fn():
        return strategy.distribute_datasets_from_function(
            lambda x: tf.data.Dataset.from_tensor_slices(data)
        )

    per_worker_dataset = coordinator.create_per_worker_dataset(
        per_worker_dataset_fn
    )
    per_worker_iter = iter(per_worker_dataset)
    print(data)
    for _ in (data * NUM_WORKERS)[:-1]:
        remote_value = coordinator.schedule(worker_fn, args=(per_worker_iter,))
    print(f"{remote_value.fetch()=}")
    # assert remote_value.fetch() == data[-1]  # the last value because worker_fn is just the iterator
    #  not sure why it seems that only the first element is executed.
    #  data=[54, 23, 42, 100, 28, 31, 53, 36, 82, 84], remote_value.fetch()=54


def start_coordinator_fetch(strategy, coordinator):
    '''
    1. Create Variable v in strategy.scope().
    2. Create dataset per worker.
    3. Run worker_fn for the dataset iteration, which assign value to the Variable v and read it.
    4. Fetch the result and expect to be one.
    '''
    def dataset_fn():
        return tf.data.Dataset.from_tensor_slices([1] * 10)

    with strategy.scope():
        v = tf.Variable(initial_value=0)

    @tf.function
    def worker_fn(iterator):
        def replica_fn(x):
            v.assign_add(x)
            return v.read_value()
        return strategy.run(replica_fn, args=(next(iterator),))

    distributed_dataset = coordinator.create_per_worker_dataset(dataset_fn)
    distributed_iterator = iter(distributed_dataset)
    result = coordinator.schedule(worker_fn, args=(distributed_iterator,))
    print(coordinator.fetch(result))
    assert coordinator.fetch(result) == 1


def start_coordinator_update_variable(strategy, coordinator):
    '''
    1. Create a variable with initial value 0.
    2. Schedule worker_fn (as tf.function) to workers.
    3. worker_fn updates the variable
    '''

    data = [randint(1, 100) for _ in range(10)]  # generate random data

    def dataset_fn():
        return tf.data.Dataset.from_tensor_slices(data)

    with strategy.scope():
        v1 = tf.Variable(initial_value=0)
        v2 = tf.Variable(initial_value=0)
        # Variable creation inside scope is intercepted by the strategy.
        # ParameterServerStrategy creates variables on the parameter servers.

    @tf.function
    def worker_fn(iterator):
        def replica_fn(x):
            v1.assign_add(x)
            return v1.read_value()
        return strategy.run(replica_fn, args=(next(iterator),))

    @tf.function
    def my_worker_fn(i):
        def replica_fn(x):
            v2.assign_add(x)
            return v2.read_value()
        return strategy.run(replica_fn, args=(i,))

    # Prepare a distribute dataset that will place datasets on the workers.
    distributed_dataset = coordinator.create_per_worker_dataset(dataset_fn)
    distributed_iterator = iter(distributed_dataset)

    for i in range(len(data * NUM_WORKERS)):
        result = coordinator.schedule(worker_fn, args=(distributed_iterator,))
        print(f"{coordinator.fetch(result)=}, {sum(data)=}")
    assert coordinator.fetch(result) == sum(data) * NUM_WORKERS

    for i in data:
        result = coordinator.schedule(my_worker_fn, args=(i,))
    print(coordinator.fetch(result))
    assert coordinator.fetch(result) == sum(data)


def distributed_variables(strategy):
    '''
    https://www.tensorflow.org/api_docs/python/tf/distribute/experimental/ParameterServerStrategy
    Variable creation with strategy.scope()

    # In this example, we're assuming having 2 ps.

    '''
    tf.debugging.set_log_device_placement(True)

    # Variables should be created inside scope to be placed on parameter servers.
    # If created outside scope such as `v1` here, it would be placed on the
    # coordinator.
    tf.Variable(initial_value=0.0)
    with strategy.scope():
        v2 = tf.Variable(initial_value=1.0)
        v3 = tf.Variable(initial_value=2.0)
        v4 = tf.Variable(initial_value=3.0)
        v5 = tf.Variable(initial_value=4.0)

    print(f"{v2=}")  # v2=<tf.Variable 'Variable:0' shape=() dtype=float32, numpy=1.0>
    # task0 = "/job:ps/replica:0/task:0/device:CPU:0"
    # task1 = "/job:ps/replica:0/task:1/device:CPU:0"

    # v2 through v5 are created in scope and are distributed on parameter servers.
    # Default placement is round-robin but the order should not be relied on.
    assert v2.device != v3.device
    assert v2.device == v4.device
    assert v3.device != v4.device
    assert v3.device == v5.device
    assert v4.device != v5.device


if __name__ == '__main__':
    main()
