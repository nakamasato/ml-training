# Movielens - Rank

## Build and push to GCP AR


Custom Container:
- https://cloud.google.com/vertex-ai/docs/training/containers-overview
- https://cloud.google.com/vertex-ai/docs/training/code-requirements


```
export PROJECT=<your project>
```

```
export REGION=asia-northeast1
export REPOSITORY=ml-training
export IMAGE=movielens
export IMAGE_TAG=0.0.1
export APP=rank
```


```
poetry export -f requirements.txt --output tensorflow/examples/movielens/requirements.txt --only=tensorflow --without-hashes
```

```
cd tensorflow/examples/movielens/
gcloud builds submit \
    --config "cloudbuild.yaml" \
    --project "${PROJECT}" \
    --substitutions="_IMAGE_TAG=${IMAGE_TAG},_IMAGE_NAME=${IMAGE},_REPOSITORY=${REPOSITORY},_REGION=${REGION},_PROJECT=${PROJECT}" \
    --gcs-source-staging-dir="gs://${PROJECT}-cloudbuild/source"
```

## Train Model

### Option1: Run on Cloud Run ✅️

```
gcloud run jobs deploy ml-training-movielens-rank --command=python --args=rank.py --memory 4Gi --cpu 2 --image "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:$IMAGE_TAG" --set-env-vars=AIP_MODEL_DIR=gs://${PROJECT}-ml-training/movielens/cloudrun/rank/model-output --set-env-vars=TF_USE_LEGACY_KERAS=1 --max-retries 0 --region $REGION --project $PROJECT
```

```
gcloud run jobs execute ml-training-movielens-rank --region $REGION --project $PROJECT
```



### Option2: Run on Vertex AI ✅️

Submit Custom Job without autopacking

- [Create Custom Job with gcloud](https://cloud.google.com/vertex-ai/docs/training/create-custom-job#create_custom_job-gcloud)
- [Envvar for special GCS dir](https://cloud.google.com/vertex-ai/docs/training/code-requirements#environment-variables)

Prepare config file

```
APP=rank envsubst < tensorflow/examples/movielens/vertexaiconfig.template.yaml > tensorflow/examples/movielens/vertexaiconfig.rank.yaml
```

Submit job

```
gcloud ai custom-jobs create --region=$REGION --display-name="movielens-rank" --config=tensorflow/examples/movielens/vertexaiconfig.rank.yaml --project $PROJECT
```

## Deploy serving

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
DEPLOYED_RANK_MODEL_ID=$(gcloud ai models describe $RANK_MODEL_ID  --region $REGION --project $PROJECT --format 'json('deployedModels')' | jq -r '.deployedModels[0].deployedModelId')
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
