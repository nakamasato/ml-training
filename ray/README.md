# [Ray](https://docs.ray.io/en/latest/)

## Version

ray: [2.3.1](https://github.com/ray-project/ray/releases/tag/ray-2.3.1)

## 1. [Getting Started](https://docs.ray.io/en/latest/ray-overview/index.html)


```
poetry run python ray/01-getting-started/task_example.py
```

## 2. Task Patterns

1. Pattern: tree of tasks (for sorting)

    ```
    poetry run python ray/02-task-pattern/task_pattern_tree.py
    ```

1. Pattern: map and reduce

    ```
    poetry run python ray/02-task-pattern/task_pattern_map_and_reduce.py
    ```

1. Pattern: limit the in flight tasks

    ```
    poetry run python ray/02-task-pattern/task_pattern_limit_in_flight_tasks.py
    ```

## Other Contents

3. [Cluster](03-cluster)
4. [Serve](04-serve)
5. [Train](05-train)
