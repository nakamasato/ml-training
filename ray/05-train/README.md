# Ray Train

## Tensorflow

`MultiWorkerMirroredStrategy`: *All workers train over different slices of input data in sync, and aggregating gradients at each step*

The script `tensorflow_example.py` is based on [Multi-worker training with Keras](https://www.tensorflow.org/tutorials/distribute/multi_worker_with_keras)


Run with local cluster:

```
python tensorflow_example.py
```

Run on a cluster:
1. Create a Ray cluster [Cluster](../03-cluster/)
    When we create a cluster, we need to add `pip install tensorflow` in `setup_command`.
1. Submit a job.
    ```
    cd ../03-cluster
    ray submit aws-config.docker.yaml ../05-train/tensorflow_example.py
    ```
