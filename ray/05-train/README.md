# Ray Train

## Simple

You can specify the trainer:

```python
def train_func(config):
    results = []
    for i in range(config["num_epochs"]):
        results.append(i)
    return results


def main(backend):
    trainer = Trainer(backend=backend, num_workers=2)
    trainer.start()
    print(trainer.run(train_func, config={"num_epochs": 2}))
    # [[0, 1], [0, 1]]
    print(trainer.run(train_func, config={"num_epochs": 5}))
    # [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
    trainer.shutdown()
```

Train with tensorflow:

```
poetry run python ray/05-train/simple_example.py -b tensorflow
```

Train with pytorch:

```
poetry run python ray/05-train/simple_example.py -b pytorch
```

## Tensorflow

`MultiWorkerMirroredStrategy`: *All workers train over different slices of input data in sync, and aggregating gradients at each step*

The script `tensorflow_example.py` is based on [Multi-worker training with Keras](https://www.tensorflow.org/tutorials/distribute/multi_worker_with_keras)


### Run with local cluster

smoke test (with in-process cluster):

```
python tensorflow_example.py --smoke-test
```

Run (You need to specify a cluster address by `--address`):

```
python tensorflow_example.py
```

### Run on a cluster:

1. Create a Ray cluster [Cluster](../03-cluster/)
    When we create a cluster, we need to add `pip install tensorflow` in `setup_command`.

1. Submit a job.
    ```
    cd ../03-cluster
    ray submit aws-config.docker.yaml ../05-train/tensorflow_example.py
    ```

## Pytorch
