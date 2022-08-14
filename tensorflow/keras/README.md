# Keras

## [fit](https://github.com/keras-team/keras/blob/v2.9.0/keras/engine/training.py#L1099-L1472)

1. all the main logics are in `with self.distribute_strategy.scope()` & `training_utils.RespectCompiledTrainableState(self)`
1. Creates a `tf.data.Dataset` and handles batch and epoch iteration with `data_adapter.get_data_handler`.
1. Set `train_function` in `make_train_function`.
1. `on_train_begin`
1. Start a for loop for **epoch** with `for epoch, iterator in data_handler.enumerate_epochs():`
    1. `on_epoch_begin(epoch)`
    1. Start a for loop for **step** with `for step in data_handler.steps():`
        1. `on_train_batch_begin(step)`
        1. Call `self.train_function(iterator)` for a step.
        1. Set end_step by `end_step = step + data_handler.step_increment`.
        1. `on_train_batch_end(end_step, logs)`
    1. Run validation
    1. `on_epoch_end`
1. `on_train_end`
1. return history

## [make_train_function](https://github.com/keras-team/keras/blob/v2.9.0/keras/engine/training.py#L998)

1. `train_function` is defined.
1. This method can be overridden to support custom training logic.
1. This method is called by `Model.fit` and `Model.train_on_batch`.
1.  Typically, this method directly controls `tf.function` and `tf.distribute.Strategy` settings, and delegates the actual training logic to `Model.train_step`.

Logic in make_train_function:
1. Define `step_function`
    ```python
    def step_function(model, iterator):
        """Runs a single training step."""

        def run_step(data):
            outputs = model.train_step(data)
            # Ensure counter is updated only if `train_step` succeeds.
            with tf.control_dependencies(_minimum_control_deps(outputs)):
                model._train_counter.assign_add(1)  # pylint: disable=protected-access
            return outputs

        if self._jit_compile:
            run_step = tf.function(
                run_step, jit_compile=True, reduce_retracing=True)
        data = next(iterator)
        outputs = model.distribute_strategy.run(run_step, args=(data,))
        outputs = reduce_per_replica(
            outputs, self.distribute_strategy, reduction='first')
        return outputs
    ```
1. Set `train_function` based on the condition:
    1. if steps_per_execution is one, train_function is step_function
        ```python
        def train_function(iterator):
            """Runs a training execution with a single step."""
            return step_function(self, iterator)
        ```
    1. else
        ```python
        def train_function(iterator, steps_per_execution):
            """Runs a training execution with multiple steps."""
            for _ in tf.range(steps_per_execution):
                outputs = step_function(self, iterator)
            return outputs
        ```
1. If `not self.run_eagerly`, wrap train_function with `tf.function` and set it to `self.train_tf_function` too.
    ```python
    if not self.run_eagerly:
        train_function = tf.function(
            train_function, reduce_retracing=True)
        self.train_tf_function = train_function
    ```
1. If cluster coordinator exists, use `ClusterCoordinator.schedule`.
    ```python
    self.train_function = lambda it: self._cluster_coordinator.schedule(  # pylint: disable=g-long-lambda
        train_function,
        args=(it, self._steps_per_execution.value()))
    ```

## [train_step](https://github.com/keras-team/keras/blob/v2.9.0/keras/engine/training.py#L861)

1. Actual train logic
1. This method can be overridden to support custom training logic.
1. This method is called by `Model.make_train_function`.

## data_handler

1. Data Handler is obtained from [get_data_handler](https://github.com/keras-team/keras/blob/07e13740fd181fc3ddec7d9a594d8a08666645f6/keras/engine/data_adapter.py#L1398):
    1. If cluster coordinator exists -> `_ClusterCoordinatorDataHandler(*args, **kwargs)`
    1. Else -> `DataHandler(*args, **kwargs)`

1. `self._inferred_steps` = `steps_per_epoch` in __init__
1. Important functions of data handler
    1. `enumerate_epochs()`
        ```python
        def enumerate_epochs(self):
            """Yields `(epoch, tf.data.Iterator)`."""
            with self._truncate_execution_to_epoch():
                data_iterator = iter(self._dataset)
                for epoch in range(self._initial_epoch, self._epochs): # initial_epoch usually zero, self._epochs <- given in __init__
                    if self._insufficient_data:  # Set by `catch_stop_iteration`.
                        break
                    if self._adapter.should_recreate_iterator():
                        data_iterator = iter(self._dataset)
                    yield epoch, data_iterator
                    self._adapter.on_epoch_end()
        ```
    1. `steps()`: yeild until current_step reaches inferred_steps (`steps_per_epoch`)

        ```python
        def steps(self):
            """Yields steps for the current epoch."""
            self._current_step = self._initial_step
            # `self._inferred_steps` can be changed by `catch_stop_iteration`.
            while (self._inferred_steps is None or
                self._current_step < self._inferred_steps):
                if self._insufficient_data:  # Set by `catch_stop_iteration`.
                    break
                original_spe = self._steps_per_execution.numpy().item()
                can_run_full_execution = (
                    original_spe == 1 or
                    self._inferred_steps is None or
                    self._inferred_steps - self._current_step >=
                    original_spe)

                if can_run_full_execution:
                    self._step_increment = original_spe - 1
                    yield self._current_step
                    self._current_step += original_spe
                else:
                    # Last partial execution.
                    steps_remaining = self._inferred_steps - self._current_step
                    self._steps_per_execution.assign(steps_remaining)
                    self._step_increment = steps_remaining - 1
                    yield self._current_step
                    self._current_step += steps_remaining
                    self._steps_per_execution.assign(original_spe)
        ```
