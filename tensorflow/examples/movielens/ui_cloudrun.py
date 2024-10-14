import os

import google.auth
import google.oauth2.id_token
import requests
import streamlit as st
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.cloud import run_v2

# https://cloud.google.com/python/docs/reference/aiplatform/latest/index.html
# https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_custom_trained_model_sample.py

st.title('MovieLens 100K')

PROJECT=os.environ["PROJECT"]
REGION = os.getenv("REGION","asia-northeast1")
SERVICE_ACCOUNT=f"movielens-ui@{PROJECT}.iam.gserviceaccount.com"
user_id = st.sidebar.selectbox("user_id", ["1", "2", "42"])


@st.cache_data
def get_id_token(url):
    """Get an ID token for the specified URL.
    If the SERVICE_ACCOUNT environment variable is set, the service account will be impersonated.

    Notes: IAM user credentials are not supported.
    """
    credentials, _ = google.auth.default()
    if not isinstance(credentials, google.oauth2.service_account.Credentials) and SERVICE_ACCOUNT is not None:
        # impersonate
        sa_credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=SERVICE_ACCOUNT,
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        credentials = impersonated_credentials.IDTokenCredentials(sa_credentials, target_audience=url, include_email=True)
        print(f"connecting with impersonated credentials {SERVICE_ACCOUNT=}")
    credentials.refresh(Request())
    return credentials.token


@st.cache_data
def get_cloud_run_service(service, location = "asia-northeast1", project = PROJECT):
    # Create a client
    client = run_v2.ServicesClient()

    # Initialize request argument(s)
    request = run_v2.GetServiceRequest(
        name=f"projects/{project}/locations/{location}/services/{service}"
    )

    # Make the request
    svc = client.get_service(request=request)

    # Handle the response
    print(svc.uri)


    # URL を取得
    print(f'Cloud Run Service URL: {svc.uri}')
    return svc


def retrieved_items(titles, scores):
    return "\n".join([f"1. `{title}` ({score:.3f})" for title, score in zip(titles, scores)])

def ranked_items(titles, scores):
    ranked = sorted([(title, score) for title, score in zip(titles, scores)], key=lambda x: x[1], reverse=True)
    return "\n".join([f"1. `{title}` ({score[0]})" for title, score in ranked])

predictions = {}
st.subheader('Retrieve')

retrieve_cloud_run_name = st.sidebar.text_input("Cloud Run Retrieve service", "movielens-retrieve")
retrieve_endpoint_id = get_cloud_run_service(retrieve_cloud_run_name).uri
st.write(retrieve_endpoint_id)
if retrieve_endpoint_id:
    url = retrieve_endpoint_id + "/v1/models/retrieve:predict"

    id_token = get_id_token(retrieve_endpoint_id)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f"Bearer {id_token}"
    }

    response = requests.post(url, headers=headers, json={"instances": [str(user_id)]})
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve: {response.text}")
    predictions = response.json()
    items = retrieved_items(predictions['predictions'][0]["output_2"], predictions['predictions'][0]["output_1"])

    st.markdown(f"""
Items:
{items}
""")


st.json(predictions, expanded=False)


st.subheader('Rank')

candidate_titles = [title for title in predictions['predictions'][0]["output_2"]] if predictions else []
instances = [{
            "user_id": str(user_id),
            "movie_title": title,
        } for title in candidate_titles]

rank_cloud_run_name = st.sidebar.text_input("Cloud Run Rank service", "movielens-rank")
rank_endpoint_id = get_cloud_run_service(rank_cloud_run_name).uri
st.write(get_cloud_run_service(rank_cloud_run_name).uri)
if rank_endpoint_id:
    url = rank_endpoint_id + "/v1/models/rank:predict"
    id_token = get_id_token(rank_endpoint_id)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f"Bearer {id_token}"
    }
    response = requests.post(
        url, headers=headers, json={"instances": instances}
    )
    predictions = response.json()
    items = ranked_items(candidate_titles, predictions['predictions'])

    st.markdown(f"""
Items:
{items}
""")

st.json(predictions, expanded=False)
