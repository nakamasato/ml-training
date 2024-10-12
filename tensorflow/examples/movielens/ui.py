import os
from typing import List

import streamlit as st
from google.cloud import aiplatform

# https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html
# https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py

st.title('MovieLens 100K')

user_id = st.sidebar.selectbox("user_id", ["1", "2", "42"])

def predict_with_model(project: str, location: str, endpoint_id: str, instances: List[dict]):
    # AI Platformの初期化
    aiplatform.init(project=project, location=location)

    # エンドポイントの取得
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)

    # 予測の実行
    predictions = endpoint.predict(instances=instances)

    return predictions

st.subheader('Retrieve')


predictions = predict_with_model(
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

st.json(predictions, expanded=False)


st.subheader('Rank')

candidate_titles = [title for title in predictions.predictions[0]["output_2"]]

predictions = predict_with_model(
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


st.json(predictions, expanded=False)
