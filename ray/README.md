# [Ray](https://docs.ray.io/en/latest/)

## Version

[v1.13.0](https://github.com/ray-project/ray/releases/tag/ray-1.13.0)

## 1. [Getting Started](https://docs.ray.io/en/latest/ray-overview/index.html)

```
pip install ray
```

```cd
python 01-getting-started/task_example.py
```

## 2. Task Patterns

1. Pattern: tree of tasks (for sorting)

    ```
    python 02-task-pattern/task_pattern_tree.py
    ```

1. Pattern: map and reduce

    ```
    python 02-task-pattern/task_pattern_map_and_reduce.py
    ```

1. Pattern: limit the in flight tasks

    ```
    python 02-task-pattern/task_pattern_limit_in_flight_tasks.py
    ```

## Other Contents

- [3. Cluster](03-cluster)
- [4. Ray Serve](04-ray-serve)
