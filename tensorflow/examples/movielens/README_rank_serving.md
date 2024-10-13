# Movielens - Serving Rank Model

## Prerequisite

Model is already saved in GCS ([Train a Rank Model](README_rank_train.md))

```
gcloud storage ls --project $PROJECT gs://${PROJECT}-ml-training/movielens/cloudrun/rank/model-output/
```

## Option1: Deploy to Vertex AI Endpoint

### [Import model from GCS](https://cloud.google.com/vertex-ai/docs/model-registry/import-model#custom-container)

With the following command, we load the model built with Cloud Run Jobs:

```
gcloud ai models upload \
  --region=$REGION \
  --display-name=movielens-rank \
  --container-image-uri=asia-docker.pkg.dev/vertex-ai-restricted/prediction/tf_opt-cpu.nightly:latest \
  --artifact-uri=gs://${PROJECT}-ml-training/movielens/cloudrun/rank/model-output/ \
  --project=$PROJECT
```

```
gcloud ai models list --project $PROJECT --region $REGION
```

### [Deploy model to endpoint](https://cloud.google.com/vertex-ai/docs/general/deployment)

Create a new endpoint (not dedicated endpoint for traffic split)

```
gcloud ai endpoints create \
  --region=$REGION \
  --display-name=movielens-rank --project $PROJECT
```

Check endpoint

```
gcloud ai endpoints list --region=$REGION --project $PROJECT
RANK_ENDPOINT_ID          DISPLAY_NAME
8479684362059644928  movielens-rank
```

Deploy the latest model

```
RANK_ENDPOINT=$(gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-rank --project $PROJECT --format="json(name)" | jq -r '.[0].name')
RANK_MODEL_ID=$(gcloud ai models list --filter=display_name=movielens-rank --region $REGION --project $PROJECT --sort-by=~versionUpdateTime --format 'json(name)' | jq -r '.[0].name' | sed 's/.*\/\(\d*\)/\1/')
```

```
gcloud ai endpoints deploy-model $RANK_ENDPOINT \
  --region=$REGION \
  --model=$RANK_MODEL_ID \
  --display-name=movielens-rank \
  --machine-type=n2-standard-2 \
  --min-replica-count=1 \
  --max-replica-count=1 \
  --traffic-split=0=100 \
  --project $PROJECT
```

> [!INFO]
> This takes 5~10 mins.

### Predict

prepare `input_data_file_rank.json`:

```json
{
    "instances": [
        {
            "user_id": "42",
            "movie_title": "M*A*S*H (1970)"
        },
        {
            "user_id": "42",
            "movie_title": "Dances with Wolves (1990)"
        },
        {
            "user_id": "42",
            "movie_title": "Speed (1994)"
        }
    ]
}
```

```
export RANK_ENDPOINT_ID=$(gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-rank --project $PROJECT --format="json(name)" | jq -r '.[0].name' | sed 's/.*\/\(\d*\)/\1/')
INPUT_DATA_FILE=tensorflow/examples/movielens/input_data_file_rank.json
```

```
curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"https://$REGION-aiplatform.googleapis.com/v1/projects/$PROJECT/locations/$REGION/endpoints/$RANK_ENDPOINT_ID:predict" \
-d "@${INPUT_DATA_FILE}"
```

```json
{
  "predictions": [
    [
      3.67746091
    ],
    [
      3.71581745
    ],
    [
      3.5969708
    ]
  ],
  "deployedModelId": "3616799519104040960",
  "model": "projects/xxxx/locations/asia-northeast1/models/7920415573568126976",
  "modelDisplayName": "movielens-rank",
  "modelVersionId": "1"
}
```

### Undeploy

```
RANK_ENDPOINT=$(gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-rank --project $PROJECT --format="json(name)" | jq -r '.[0].name')
RANK_MODEL_ID=$(gcloud ai models list --filter=display_name=movielens-rank --region $REGION --project $PROJECT --sort-by=~versionUpdateTime --format 'json(name)' | jq -r '.[0].name' | sed 's/.*\/\(\d*\)/\1/')
DEPLOYED_RANK_MODEL_ID=$(gcloud ai models describe $RANK_MODEL_ID --region $REGION --project $PROJECT --format 'json('deployedModels')' | jq -r '.deployedModels[0].deployedModelId')
gcloud ai endpoints undeploy-model $RANK_ENDPOINT \
    --project=$PROJECT \
    --region=$REGION \
    --deployed-model-id=$DEPLOYED_RANK_MODEL_ID
```

```
gcloud ai endpoints delete $RANK_ENDPOINT \
    --project=$PROJECT \
    --region=$REGION
```

## Option2: Deploy to Cloud Run with TFX Serving

- https://www.tensorflow.org/tfx/serving/serving_basic
- https://keras.io/examples/keras_recipes/tf_serving/

Build serving container (copy the model from gcs to docker image)

```
cd tensorflow/examples/movielens/
gcloud builds submit \
    --config "cloudbuild.serving.yaml" \
    --project "${PROJECT}" \
    --substitutions="_IMAGE_TAG=${IMAGE_TAG},_IMAGE_NAME=movielens-rank,_REPOSITORY=${REPOSITORY},_REGION=${REGION},_PROJECT=${PROJECT},_EXPORT_BUCKET=gs://$PROJECT-ml-training/movielens/cloudrun/rank/" \
    --gcs-source-staging-dir="gs://${PROJECT}-cloudbuild/source"
```

This copis model from `gs://$PROJECT-ml-training/movielens/cloudrun/rank/` to `models/` dir and then, the image contains the model files under `/models/` (e.g. `/models/rank/1/`)


```
gcloud run deploy movielens-rank \
    --image=$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/movielens-rank:$IMAGE_TAG \
    --port=8501 \
    --region=$REGION \
    --execution-environment=gen2 \
    --no-allow-unauthenticated \
    --project=$PROJECT \
    --set-env-vars=MODEL_NAME="rank" \
    --set-env-vars=MODEL_BASE_PATH=/models/
```

```
RANK_URL=$(gcloud run services describe movielens-rank \
    --region=$REGION \
    --project=$PROJECT --format json | jq -r '.status.url'); echo $RANK_URL
```


```
curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
"$RANK_URL/v1/models/rank:predict" \
-d "@tensorflow/examples/movielens/input_data_file_rank.json"
```

Result ✅️

```
{
    "predictions": [[3.55253816], [3.61419201], [3.52277851]
    ]
}
```

## Ref

- https://github.com/guillaumeblaquiere/cloudrun-tensorflow-prediction/tree/master
