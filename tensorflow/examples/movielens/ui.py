import os
from typing import List

import google.auth
import requests
import streamlit as st
from google.auth.transport.requests import Request
from google.cloud import aiplatform

# https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html
# https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py

st.title('MovieLens 100K')

user_id = st.sidebar.selectbox("user_id", ["1", "2", "42"])
endpoint_type = st.sidebar.selectbox("endpoint_type", ["Vertex AI endpoint", "Cloud Run"], index=1)

def predict_with_vertex_ai_endpoint(project: str, location: str, endpoint_id: str, instances: List[dict]):
    # AI Platformの初期化
    aiplatform.init(project=project, location=location)

    # エンドポイントの取得
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)

    # 予測の実行
    predictions = endpoint.predict(instances=instances)

    return predictions

st.subheader('Retrieve')

if endpoint_type == "Vertex AI endpoint":
    predictions = predict_with_vertex_ai_endpoint(
        project=os.environ["PROJECT"],
        endpoint_id=os.environ["RETRIEVE_ENDPOINT_ID"],
        location=os.getenv("REGION","asia-northeast1"),
        instances=[str(user_id)],
    )
    print(predictions)

    items = "\n".join([f"1. `{title}` ({score:.3f})" for title, score in zip(predictions.predictions[0]["output_2"], predictions.predictions[0]["output_1"])])

    st.sidebar.markdown(f"""
## Retrieve:

- model_id: {predictions.deployed_model_id}
- model_version: {predictions.model_version_id}
- metadata: {predictions.metadata}
- model_resource_name: {predictions.model_resource_name}
""")

    st.markdown(f"""
Items:
{items}
""")

else:
    retrieve_endpoint = st.sidebar.text_input("Cloud Run Retrieve endpoint")
    st.write(retrieve_endpoint)
    if retrieve_endpoint:
        url = retrieve_endpoint + "/v1/models/retrieve:predict"
        st.write(url)
        print(url)
        credentials, project = google.auth.default()
        credentials.refresh(Request())
        headers = {
            "Content-Type": "application/json",
            'Authorization': f"Bearer {credentials.token}"
        }

        response = requests.post(url, headers=headers, json={"instances": [str(user_id)]})
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve: {response.text}")
        st.write(response.json())
        predictions = response.json()


st.json(predictions, expanded=False)


st.subheader('Rank')

candidate_titles = [title for title in (predictions.predictions[0]["output_2"] if endpoint_type == "Vertex AI endpoint" else predictions['predictions'][0]["output_2"])]

if endpoint_type == "Vertex AI endpoint":
    predictions = predict_with_vertex_ai_endpoint(
        project=os.environ["PROJECT"],
        endpoint_id=os.environ["RANK_ENDPOINT_ID"],
        location=os.getenv("REGION","asia-northeast1"),
        instances=[{
            "user_id": str(user_id),
            "movie_title": title,
        } for title in candidate_titles],
    )

    print(predictions.predictions[0])
    ranked = sorted([(title, score) for title, score in zip(candidate_titles, predictions.predictions)], key=lambda x: x[1], reverse=True)
    items = "\n".join([f"1. `{title}` ({score[0]})" for title, score in ranked])

    st.sidebar.markdown(f"""
## Rank:

- model_id: {predictions.deployed_model_id}
- model_version: {predictions.model_version_id}
- metadata: {predictions.metadata}
- model_resource_name: {predictions.model_resource_name}
""")

    st.markdown(f"""
Items:
{items}
""")
else:
    rank_endpoint = st.sidebar.text_input("Cloud Run Rank endpoint")

    if rank_endpoint:
        url = rank_endpoint + "/v1/models/rank:predict"
        credentials, project = google.auth.default()
        credentials.refresh(Request())
        headers = {
            "Content-Type": "application/json",
            'Authorization': f"Bearer {credentials.token}"
        }
        response = requests.post(
            url, headers=headers, json={"instances": [{"user_id": str(user_id), "movie_title": title} for title in candidate_titles]}
        )
        predictions = response.json()
        st.json(predictions)


st.json(predictions, expanded=False)
