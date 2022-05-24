import ray
from ray import serve
from transformers import pipeline


def summarize(text):
    summarizer = pipeline("summarization", model="t5-small")
    summary_list = summarizer(text)
    summary = summary_list[0]["summary_text"]
    return summary


ray.init(address="auto", namespace="serve") # init or connect to cluster

serve.start(detached=True) # start serving


@serve.deployment
def router(request):
    txt = request.query_params["txt"]
    return summarize(txt)


router.deploy()
