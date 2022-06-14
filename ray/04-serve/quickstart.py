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
