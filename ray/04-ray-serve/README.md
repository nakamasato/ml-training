# Ray Serve
## 1. Quickstart

1. Install `ray[serve]`

    ```
    pip install "ray[serve]"
    ```
1. Prepare `quickstart.py`.

    ```python
    from time import sleep

    import ray
    from ray import serve

    ray.init()  # 1. init cluster

    serve.start()  # 2. serve start


    @serve.deployment  # 3. define deployment
    class Counter:
        def __init__(self):
            self.count = 0

        def __call__(self, request):
            self.count += 1
            return {"count": self.count}


    Counter.deploy()  # 4. deploy
    sleep(100)
    ```

1. Run

    ```
    python quickstart.py
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

    Get the counter:
    ```
    curl -X GET localhost:8000/Counter/
    {"count": 0}
    ```

You can also try an extended quickstart with `quickstart_extended.py`

## 2. [End-to-End Tutorial](https://docs.ray.io/en/latest/serve/end_to_end_tutorial.html)

Summarize a long English text with `transformers` library.

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

    1. Send request (either via HTTP or Python).

        ```
        python router_client.py
        ----- HTTP START -----
        two astronauts steered their fragile lunar module safely and smoothly to the historic landing . the first men to reach the moon -- Armstrong and his co-pilot, col. Edwin E. Aldrin Jr. of the air force -- brought their ship to rest on a level, rock-strewn plain .
        ----- HTTP END -----
        ----- ServeHandle START -----
        two astronauts steered their fragile lunar module safely and smoothly to the historic landing . the first men to reach the moon -- Armstrong and his co-pilot, col. Edwin E. Aldrin Jr. of the air force -- brought their ship to rest on a level, rock-strewn plain .
        ----- ServeHandle END -----
        ```

1. Stop the ray cluster

    ```
    ray stop
    ```

Notes:

1. You can create deployment either with a function or a class using `@serve.deployment` annotation.
1. If you want to support both HTTP request and ServeHandle request, it's recommended to use a class for the deployment to separate a internal function that can be called via ServeHandle. ([ServeHandle for deployment created with a function with query_params?](https://discuss.ray.io/t/servehandle-for-deployment-created-with-a-function-with-query-params/6291))
    Example: `summarize` function in `Router` class.
    ```python
    print(ray.get(handle.summarize.remote(article_text)))
    ```

## 3. [Model Composition](https://docs.ray.io/en/latest/serve/ml-models.html#serve-model-composition)

Run

```
python model_composition.py
```


<details>

```
python model_composition.py
2022-05-26 09:54:33,004 INFO services.py:1456 -- View the Ray dashboard at http://127.0.0.1:8265
(ServeController pid=33393) 2022-05-26 09:54:40,580     INFO checkpoint_path.py:15 -- Using RayInternalKVStore for controller checkpoint and recovery.
(ServeController pid=33393) 2022-05-26 09:54:40,688     INFO http_state.py:106 -- Starting HTTP proxy with name 'SERVE_CONTROLLER_ACTOR:iLqOel:SERVE_PROXY_ACTOR-node:127.0.0.1-0' on node 'node:127.0.0.1-0' listening on '127.0.0.1:8000'
2022-05-26 09:54:42,210 INFO api.py:794 -- Started Serve instance in namespace 'ff4601f8-69e6-4998-a739-04c85414beaa'.
(HTTPProxyActor pid=33400) INFO:     Started server process [33400]
2022-05-26 09:54:42,244 INFO api.py:615 -- Updating deployment 'model_one'. component=serve deployment=model_one
(ServeController pid=33393) 2022-05-26 09:54:42,276     INFO deployment_state.py:1210 -- Adding 1 replicas to deployment 'model_one'. component=serve deployment=model_one
2022-05-26 09:54:44,353 INFO api.py:630 -- Deployment 'model_one' is ready at `http://127.0.0.1:8000/model_one`. component=serve deployment=model_one
2022-05-26 09:54:44,361 INFO api.py:615 -- Updating deployment 'model_two'. component=serve deployment=model_two
(ServeController pid=33393) 2022-05-26 09:54:44,449     INFO deployment_state.py:1210 -- Adding 1 replicas to deployment 'model_two'. component=serve deployment=model_two
2022-05-26 09:54:46,387 INFO api.py:630 -- Deployment 'model_two' is ready at `http://127.0.0.1:8000/model_two`. component=serve deployment=model_two
2022-05-26 09:54:46,398 INFO api.py:615 -- Updating deployment 'ComposedModel'. component=serve deployment=ComposedModel
(ServeController pid=33393) 2022-05-26 09:54:46,423     INFO deployment_state.py:1210 -- Adding 1 replicas to deployment 'ComposedModel'. component=serve deployment=ComposedModel
2022-05-26 09:54:49,431 INFO api.py:630 -- Deployment 'ComposedModel' is ready at `http://127.0.0.1:8000/composed`. component=serve deployment=ComposedModel
(model_one pid=33403) Model 1 called with data:b'Hey!'
(model_two pid=33404) Model 2 called with data:b'Hey!'
{'model_used: 1 & 2;  score': 0.5288903723877777}
{'model_used: 1 ; score': 0.45322933175804514}
{'model_used: 1 ; score': 0.16603929376288173}
{'model_used: 1 & 2;  score': 0.9928666980845869}
(model_one pid=33403) Model 1 called with data:b'Hey!'
(model_one pid=33403) Model 1 called with data:b'Hey!'
(model_one pid=33403) Model 1 called with data:b'Hey!'
(model_one pid=33403) Model 1 called with data:b'Hey!'
(model_two pid=33404) Model 2 called with data:b'Hey!'
(model_two pid=33404) Model 2 called with data:b'Hey!'
{'model_used: 1 & 2;  score': 0.83580165395007}
{'model_used: 1 & 2;  score': 0.8273714159873894}
{'model_used: 1 ; score': 0.4718116502142262}
{'model_used: 1 & 2;  score': 0.8397308071154511}
```

</details>

## References

1. https://medium.com/distributed-computing-with-ray/the-simplest-way-to-serve-your-nlp-model-in-production-with-pure-python-d42b6a97ad55
1. https://vishnudeva.medium.com/scaling-applications-on-kubernetes-with-ray-23692eb2e6f0
