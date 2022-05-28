import ray
import requests
from fastapi import FastAPI
from ray import serve

# start a Ray cluster
ray.init()

# start Ray Serve runtime
serve.start()  # you can set 'detached=True' to keep Ray Serve running in the background

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

# http request
print(requests.get("http://127.0.0.1:8000/Counter").text)
print(requests.get("http://127.0.0.1:8000/Counter/incr").text)
print(requests.get("http://127.0.0.1:8000/Counter/incr").text)
print(requests.get("http://127.0.0.1:8000/Counter/decr").text)
