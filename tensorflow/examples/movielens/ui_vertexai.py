import os
from typing import List

import google.auth
import google.oauth2.id_token
import requests
import streamlit as st
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.cloud import aiplatform, run_v2

# https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html
# https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py

st.title('MovieLens 100K')

PROJECT=os.environ["PROJECT"]
REGION = os.getenv("REGION","asia-northeast1")
user_id = st.sidebar.selectbox("user_id", ["1", "2", "42"])


def retrieved_items(titles, scores):
    return "\n".join([f"1. `{title}` ({score:.3f})" for title, score in zip(titles, scores)])

def ranked_items(titles, scores):
    ranked = sorted([(title, score) for title, score in zip(titles, scores)], key=lambda x: x[1], reverse=True)
    return "\n".join([f"1. `{title}` ({score[0]})" for title, score in ranked])

predictions = {}


def predict_with_vertex_ai_endpoint(project: str, location: str, endpoint_id: str, instances: List[dict]):
    # AI Platformの初期化
    aiplatform.init(project=project, location=location)

    # エンドポイントの取得
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)

    # 予測の実行
    predictions = endpoint.predict(instances=instances)

    return predictions


@st.cache_data
def get_vertex_ai_endpoint_id(endpoint_name: str, order_by: str = "~updateTime"):
    """Get the Vertex AI endpoint by the endpoint Name.
    gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-rank --project $PROJECT --format="json(name)" | jq -r '.[0].name'
    """
    # AI Platformの初期化
    aiplatform.init(project=PROJECT, location=REGION)

    # エンドポイントの取得
    endpoint = aiplatform.Endpoint.list(filter=f"display_name={endpoint_name}")[0]

    return endpoint.name

st.subheader('Retrieve')


retrieve_endpoint_name = st.sidebar.text_input("Vertex AI Endpoint for Retrieve", "movielens-retrieve")
if retrieve_endpoint_name:
    retrieve_endpoint_id = get_vertex_ai_endpoint_id(retrieve_endpoint_name)
    st.write(retrieve_endpoint_id)
    predictions = predict_with_vertex_ai_endpoint(
        project=PROJECT,
        endpoint_id=retrieve_endpoint_id,
        location=REGION,
        instances=[str(user_id)],
    )
    print(predictions)

    st.sidebar.markdown(f"""
## Retrieve:

- model_id: {predictions.deployed_model_id}
- model_version: {predictions.model_version_id}
- metadata: {predictions.metadata}
- model_resource_name: {predictions.model_resource_name}
""")

    items = retrieved_items(predictions.predictions[0]["output_2"], predictions.predictions[0]["output_1"])

    st.markdown(f"""
Items:
{items}
""")


st.json(predictions, expanded=False)

st.subheader('Rank')

candidate_titles = [title for title in predictions.predictions[0]["output_2"] ] if predictions else []
instances = [{
    "user_id": str(user_id),
    "movie_title": title,
} for title in candidate_titles]

rank_endpoint_name = st.sidebar.text_input("Cloud Run Rank service", "movielens-rank")
if rank_endpoint_name:
    rank_endpoint_id = get_vertex_ai_endpoint_id(rank_endpoint_name)
    st.write(rank_endpoint_id)
    predictions = predict_with_vertex_ai_endpoint(
        project=PROJECT,
        endpoint_id=rank_endpoint_id,
        location=REGION,
        instances=instances,
    )
    print(predictions.predictions[0])


    st.sidebar.markdown(f"""
## Rank:

- model_id: {predictions.deployed_model_id}
- model_version: {predictions.model_version_id}
- metadata: {predictions.metadata}
- model_resource_name: {predictions.model_resource_name}
""")
    items = ranked_items(candidate_titles, predictions.predictions)

    st.markdown(f"""
Items:
{items}
""")

st.json(predictions, expanded=False)
