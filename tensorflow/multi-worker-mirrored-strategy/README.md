# Multi-worker Mirrored Strategy

## Run

1. run on single worker
    ```
    poetry run python tensorflow/multi-worker-mirrored-strategy/run_with_single_workers.py
    ```
1. run on multi workers (2 workers)

    task 0:
    ```
    TF_CONFIG='{"cluster": {"worker": ["localhost:12345", "localhost:23456"]}, "task": {"type": "worker", "index": 0} }' python run_with_multi_worker.py
    ```

    task 1:
    ```
    TF_CONFIG='{"cluster": {"worker": ["localhost:12345", "localhost:23456"]}, "task": {"type": "worker", "index": 1} }' python run_with_multi_worker.py
    ```
