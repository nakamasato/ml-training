# Ray Serve
## Quickstart

1. Install `ray[serve]`

    ```
    pip install "ray[serve]"
    ```
1. Learn.

    ```python
    import ray
    from ray import serve

    ray.init() # 1. init cluster

    serve.start() # 2. serve start

    @serve.deployment # 3. define deployment
    class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self, request):
        self.count += 1
        return {"count": self.count}

    Counter.deploy() # 4. deploy
    ```

1. Run

    ```
    python serve_quickstart.py
    ```

    <details>

    ```
    2022-05-22 06:46:24,611 INFO services.py:1456 -- View the Ray dashboard at http://127.0.0.1:8265
    (ServeController pid=27612) 2022-05-22 06:46:29,494     INFO checkpoint_path.py:15 -- Using RayInternalKVStore for controller checkpoint and recovery.
    (ServeController pid=27612) 2022-05-22 06:46:29,609     INFO http_state.py:106 -- Starting HTTP proxy with name 'SERVE_CONTROLLER_ACTOR:DylMax:SERVE_PROXY_ACTOR-node:127.0.0.1-0' on node 'node:127.0.0.1-0' listening on '127.0.0.1:8000'
    2022-05-22 06:46:30,915 INFO api.py:794 -- Started Serve instance in namespace '9c985508-1c83-47f5-a078-ca1faa3ed450'.
    (HTTPProxyActor pid=27613) INFO:     Started server process [27613]
    2022-05-22 06:46:30,934 INFO api.py:615 -- Updating deployment 'Counter'. component=serve deployment=Counter
    (ServeController pid=27612) 2022-05-22 06:46:31,015     INFO deployment_state.py:1210 -- Adding 1 replicas to deployment 'Counter'. component=serve deployment=Counter
    2022-05-22 06:46:35,004 INFO api.py:630 -- Deployment 'Counter' is ready at `http://127.0.0.1:8000/Counter`. component=serve deployment=Counter
    ```

    </details>

1. Check on http://127.0.0.1:8000/Counter.

    ```
    curl -X GET localhost:8000/Counter/
    ```

    ```json
    {"count": 0}
    ```

    ```
    curl -X GET localhost:8000/Counter/incr
    ```

    ```
    curl -X GET localhost:8000/Counter/decr
    ```

## [End-to-End Tutorial](https://docs.ray.io/en/latest/serve/end_to_end_tutorial.html)

1. Install libraries.
    Use https://huggingface.co/docs/transformers/index.

    ```
    pip install transformers
    pip install 'transformers[torch]'
    ```

1. Run locally.

    ```
    python local_model.py
    ```

    <details>

    ```
    Downloading: 100%|█████████████████████████████████████████████████████████| 231M/231M [00:43<00:00, 5.61MB/s]
    Downloading: 100%|██████████████████████████████████████████████████████████| 773k/773k [00:02<00:00, 298kB/s]
    Downloading: 100%|████████████████████████████████████████████████████████| 1.32M/1.32M [00:07<00:00, 184kB/s]
    /Users/nakamasato/.pyenv/versions/3.9.0/lib/python3.9/site-packages/transformers/models/t5/tokenization_t5_fast.py:155: FutureWarning: This tokenizer was incorrectly instantiated with a model max length of 512 which will be corrected in Transformers v5.
    For now, this behavior is kept to avoid breaking backwards compatibility when padding/encoding with `truncation is True`.
    - Be aware that you SHOULD NOT rely on t5-small automatically truncating your input to 512 when padding/encoding.
    - If you want to encode/pad to sequences longer than 512 you can either instantiate this tokenizer with `model_max_length` or pass `max_length` when encoding/padding.
    - To avoid this warning, please instantiate this tokenizer with `model_max_length` set to your preferred value.
      warnings.warn(
    two astronauts steered their fragile lunar module safely and smoothly to the historic landing . the first men to reach the moon -- Armstrong and his co-pilot, col. Edwin E. Aldrin Jr. of the air force -- brought their ship to rest on a level, rock-strewn plain .
    ```

    </details>

1. Deploy this model using Ray Serve

    1. Create local ray cluster.

        ```
        ray start --head
        ```

    1. Run.

        ```
        python model_on_ray_serve.py
        ```

    1. Send request via HTTP.

        ```
        python router_client.py
        two astronauts steered their fragile lunar module safely and smoothly to the historic landing . the first men to reach the moon -- Armstrong and his co-pilot, col. Edwin E. Aldrin Jr. of the air force -- brought their ship to rest on a level, rock-strewn plain .
        ```

1. Stop the ray cluster

    ```
    ray stop
    ```


## References

1. https://medium.com/distributed-computing-with-ray/the-simplest-way-to-serve-your-nlp-model-in-production-with-pure-python-d42b6a97ad55
