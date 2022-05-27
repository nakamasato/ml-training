import ray
from ray import serve
from transformers import pipeline


def summarize(text):
    summarizer = pipeline("summarization", model="t5-small")
    summary_list = summarizer(text)
    summary = summary_list[0]["summary_text"]
    return summary


# init or connect to cluster
ray.init(address="auto", namespace="serve")

# start serving
serve.start(detached=True)


# function with serve.deployment
@serve.deployment
def router(request):
    txt = request.query_params["txt"]
    return summarize(txt)


router.deploy()


# class with serve.deployment
@serve.deployment
class Router:

    # best practice to separate a function
    # when supporting access via both HTTP and ServeHandle
    def summarize(self, txt):
        return summarize(txt)

    def __call__(self, request):
        txt = request.query_params["txt"]
        return self.summarize(txt)


Router.deploy()
