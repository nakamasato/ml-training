from time import sleep
from fastapi import FastAPI
import ray
from ray import serve

# start a Ray cluster
ray.init()

# start Ray Serve runtime
serve.start()

# serve this class behind an HTTP endpoint using Ray Serve.
app = FastAPI()


@serve.deployment
@serve.ingress(app)
class Counter:
    def __init__(self):
        self.count = 0

    @app.get("/")
    def get(self):
        return {"count": self.count}

    @app.get("/incr")
    def incr(self):
        self.count += 1
        return {"count": self.count}

    @app.get("/decr")
    def decr(self):
        self.count -= 1
        return {"count": self.count}


# deploy
Counter.deploy()

sleep(100)
