# [Movielens](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

## Version

- tensorflow: 2.17.0
- keras: 2.17.0 (`poetry add tf_keras --group tensorflow`)

## Run

### retrieve

`TF_USE_LEGACY_KERAS=1` is set in `.env` (This is necessary because https://github.com/tensorflow/recommenders/issues/712)

```
poetry run python tensorflow/examples/movielens/retrieve.py
```

### rank

train Rank model and save the model

```
WRAPT_DISABLE_EXTENSIONS=1 poetry run python tensorflow/examples/movielens/rank.py
```

## Data

### ratings

1. bucketized_user_age
1. movie_genres
1. movie_id
1. movie_title
1. raw_user_age
1. timestamp
1. user_gender
1. user_id
1. user_occupation_label
1. user_occupation_text
1. user_rating
1. user_zip_code

### movies

1. movie_genres
1. movie_id
1. movie_title


## Basic Model

1. user_id
1. movie_title

## Embedding

`StringLookup` だと未知のユーザに対して、適当な値を作れない

```py
>>> user_ids_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
>>> user_ids_vocabulary
<StringLookup name=string_lookup_1, built=False>
>>> user_ids_vocabulary.adapt(["uid1", "uid2"])
>>> user_ids_vocabulary
<StringLookup name=string_lookup_1, built=False>
>>> user_ids_vocabulary("uid1")
<tf.Tensor: shape=(), dtype=int64, numpy=2>
>>> user_ids_vocabulary("uid2")
<tf.Tensor: shape=(), dtype=int64, numpy=1>
>>> user_ids_vocabulary("uid3")
<tf.Tensor: shape=(), dtype=int64, numpy=0>
>>> user_ids_vocabulary("uid4")
<tf.Tensor: shape=(), dtype=int64, numpy=0>
>>> user_ids_vocabulary("uid5")
<tf.Tensor: shape=(), dtype=int64, numpy=0>
```

```py
user_model(tf.constant("uid2")) # embeddingを取得できる
```

## Build and push to GCP AR

Custom Container:
- https://cloud.google.com/vertex-ai/docs/training/containers-overview
- https://cloud.google.com/vertex-ai/docs/training/code-requirements

```
export PROJECT=
```

```
export REGION=asia-northeast1
export REPOSITORY=ml-training
export IMAGE=movielens-retrieve
export IMAGE_TAG=0.0.1
```

export PROJECT=

```
poetry export -f requirements.txt --output tensorflow/examples/movielens/requirements.txt --only=tensorflow --without-hashes
```

build locally

```
pack build --platform linux/amd64 --builder heroku/builder:22 $IMAGE --path tensorflow/examples/movielens
```

run locally

```
docker run --rm $IMAGE python retrieve.py
```

build and publish (❌)

mac: `--platform linux/amd64`
linux: `--platform linux/amd64`

```
gcloud auth login
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
pack build "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:$IMAGE_TAG" \
    --env "GOOGLE_ENTRYPOINT='web: python retrieve.py'" \
    --tag "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:latest" \
    --path tensorflow/examples/movielens \
    --builder heroku/builder:22 \
    --publish
```

```
docker buildx build --platform linux/amd64 -f tensorflow/examples/movielens/Dockerfile -t $IMAGE:$IMAGE_TAG tensorflow/examples/movielens
docker tag $IMAGE:$IMAGE_TAG "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:$IMAGE_TAG"
docker push "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:$IMAGE_TAG"
```

> [!WARN]
> Local build didn't work due to the following error
> -> `terminated: Application failed to start: "/usr/local/bin/python" exec format error`

```
cd tensorflow/examples/movielens/
gcloud builds submit \
    --config "cloudbuild.yaml" \
    --project "${PROJECT}" \
    --substitutions="_IMAGE_TAG=${IMAGE_TAG},_IMAGE_NAME=${IMAGE},_REPOSITORY=${REPOSITORY},_REGION=${REGION},_PROJECT=${PROJECT}" \
    --gcs-source-staging-dir="gs://${PROJECT}-cloudbuild/source"
```

## Run on Cloud Run ✅️

memo: `--command=python --args=retrieve.py --set-env-vars=PYTHONPATH=/workspace/` for image built by buildpacks

```
gcloud run jobs deploy ml-training-movielens-retrieve --memory 4Gi --cpu 2 --image "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:$IMAGE_TAG" --set-env-vars=AIP_MODEL_DIR=gs://${PROJECT}-ml-training/movielens/cloudrun/model-output --set-env-vars=TF_USE_LEGACY_KERAS=1 --max-retries 0 --region $REGION --project $PROJECT
```

```
gcloud run jobs execute ml-training-movielens-retrieve --region $REGION --project $PROJECT
```

> [!WARN]
> `"ValueError: Cannot convert '('c', 'o', 'u', 'n', 't', 'e', 'r')' to a shape. Found invalid entry 'c' of type '<class 'str'>'. "`

-> `--set-env-vars=TF_USE_LEGACY_KERAS=1` is necessary ✅️

You can check the saved model:

```
gcloud storage ls "gs://${PROJECT}-ml-training/movielens/cloudrun/model-output/"
gs://PROJECT-ml-training/movielens/cloudrun/model-output/

gs://PROJECT-ml-training/movielens/cloudrun/model-output/:
gs://PROJECT-ml-training/movielens/cloudrun/model-output/
gs://PROJECT-ml-training/movielens/cloudrun/model-output/fingerprint.pb
gs://PROJECT-ml-training/movielens/cloudrun/model-output/keras_metadata.pb
gs://PROJECT-ml-training/movielens/cloudrun/model-output/saved_model.pb
gs://PROJECT-ml-training/movielens/cloudrun/model-output/assets/
gs://PROJECT-ml-training/movielens/cloudrun/model-output/model/
gs://PROJECT-ml-training/movielens/cloudrun/model-output/variables/
```

## Run on VertexAI ✅️

### Train model

> [!WARN]
>
> Local Run (❌️ `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested`)
>
> ```
> gcloud ai custom-jobs local-run --executor-image-uri="$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$IMAGE:$IMAGE_TAG" --project $PROJECT
> ```

Submit Custom Job without autopacking

- [Create Custom Job with gcloud](https://cloud.google.com/vertex-ai/docs/training/create-custom-job#create_custom_job-gcloud)
- [Envvar for special GCS dir](https://cloud.google.com/vertex-ai/docs/training/code-requirements#environment-variables)

Prepare config file

```
envsubst < tensorflow/examples/movielens/vertexaiconfig.template.yaml > tensorflow/examples/movielens/vertexaiconfig.yaml
```

Submit job

```
gcloud ai custom-jobs create --region=$REGION --display-name="movielens-retrieve" --config=tensorflow/examples/movielens/vertexaiconfig.yaml --project $PROJECT
```

### [Import model from GCS](https://cloud.google.com/vertex-ai/docs/model-registry/import-model#custom-container)

```
gcloud ai models upload \
  --region=$REGION \
  --display-name=movielens-retrieve \
  --container-image-uri=asia-docker.pkg.dev/vertex-ai-restricted/prediction/tf_opt-cpu.nightly:latest \
  --artifact-uri=gs://${PROJECT}-ml-training/movielens/vertexai/model-output/model/ \
  --project=$PROJECT
```

```
gcloud ai models list --project $PROJECT --region $REGION
MODEL_ID             DISPLAY_NAME
2548324905556901888  movielens-retrieve
```

- **artifact-uri**: the directory that contains your model artifacts (`saved_model.pb` for TensorFlow)
- **container image uri**: The URI of the container image to use for serving predictions.
    - https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers
    - https://cloud.google.com/vertex-ai/docs/predictions/optimized-tensorflow-runtime

### [Deploy model to endpoint](https://cloud.google.com/vertex-ai/docs/general/deployment)

Here, we deploy the model to a dedicated endpoint: ❌️

```
curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d '{"display_name": "movielens-retrieve", "dedicatedEndpointEnabled": true}' \
https://$REGION-aiplatform.googleapis.com/v1/projects/$PROJECT/locations/$REGION/endpoints
```

> [!WARN] The create operation is invisible and it takes time to get visible by `gcloud ai endpoints list --region $REGION --project $PROJECT`.

<details><summary>alternatively</summary>

Create a new endpoint

```
gcloud ai endpoints create \
  --region=$REGION \
  --display-name=movielens-retrieve --project $PROJECT
```

</details>

Check the endpoint

```
gcloud ai endpoints list --region=$REGION --project $PROJECT
ENDPOINT_ID          DISPLAY_NAME
2891702386911346688  movielens-retrieve
```

Deploy the model

```
ENDPOINT=$(gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-retrieve --project $PROJECT --format="json(name)" | jq -r '.[0].name')
MODEL_ID=$(gcloud ai models list --filter=display_name=movielens-retrieve --region $REGION --project $PROJECT --format 'json(name)' | jq -r '.[0].name' | sed 's/.*\/\(\d*\)/\1/')
```

```
gcloud ai endpoints deploy-model $ENDPOINT \
  --region=$REGION \
  --model=$MODEL_ID \
  --display-name=movielens-retrieve \
  --machine-type=n2-standard-2 \
  --min-replica-count=1 \
  --max-replica-count=1 \
  --traffic-split=0=100 \
  --project $PROJECT
```

> [!INFO]
> This takes 5~10 mins.


### Predict

prepare `input_data_file.json`:

```json
{
    "instances": [
         "42"
    ]
}
```

```
ENDPOINT_ID=$(gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-retrieve --project $PROJECT --format="json(name)" | jq -r '.[0].name' | sed 's/.*\/\(\d*\)/\1/')
INPUT_DATA_FILE=tensorflow/examples/movielens/input_data_file.json
```

```
curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"https://$REGION-aiplatform.googleapis.com/v1/projects/$PROJECT/locations/$REGION/endpoints/$ENDPOINT_ID:predict" \
-d "@${INPUT_DATA_FILE}"
```

Result:

```
{
  "predictions": [
    {
      "output_2": [
        "Rent-a-Kid (1995)",
        "Far From Home: The Adventures of Yellow Dog (1995)",
        "Just Cause (1995)",
        "Land Before Time III: The Time of the Great Giving (1995) (V)",
        "Nell (1994)",
        "Two if by Sea (1996)",
        "Jack (1996)",
        "Panther (1995)",
        "House Arrest (1996)",
        "Conan the Barbarian (1981)"
      ],
      "output_1": [
        3.94025946,
        3.47775483,
        3.4017539,
        3.32554197,
        2.95510435,
        2.63177681,
        2.61488819,
        2.61403036,
        2.58744907,
        2.54093599
      ]
    }
  ],
  "deployedModelId": "535000367843246080",
  "model": "projects/xxxx/locations/asia-northeast1/models/2548324905556901888",
  "modelDisplayName": "movielens-retrieve",
  "modelVersionId": "1"
}
```

![](vertexai-test.png)

### Undeploy

```
ENDPOINT=$(gcloud ai endpoints list --region=$REGION --filter=display_name=movielens-retrieve --project $PROJECT --format="json(name)" | jq -r '.[0].name')
DEPLOYED_MODEL_ID=$(gcloud ai models describe $MODEL_ID  --region $REGION --project $PROJECT --format 'json('deployedModels')' | jq -r '.deployedModels[].deployedModelId')
gcloud ai endpoints undeploy-model $ENDPOINT \
    --project=$PROJECT \
    --region=$REGION \
    --deployed-model-id=$DEPLOYED_MODEL_ID
```


## Errors

1. [ValueError: Cannot convert '('c', 'o', 'u', 'n', 't', 'e', 'r')' to a shape. Found invalid entry 'c' of type '<class 'str'>' tfrs.metrics.FactorizedTopK](https://github.com/tensorflow/recommenders/issues/712): to be resolved by https://github.com/tensorflow/recommenders/pull/717 or `TF_USE_LEGACY_KERAS=1` with `poetry add tf_keras --group tensorflow`

1. `ValueError: Only input tensors may be passed as positional arguments. The following argument value should be passed as a keyword argument: 42 (of type <class 'str'>)`
    ```diff
    - print(RankingModel()((["42"], ["One Flew Over the Cuckoo's Nest (1975)"])))
    + user_id_tensor = tf.convert_to_tensor(["42"])
    + movie_title_tensor = tf.convert_to_tensor(["One Flew Over the Cuckoo's Nest (1975)"])
    + print(RankingModel()((user_id_tensor, movie_title_tensor)))
    ```

1. `ValueError: TensorFlowTrainer.make_train_function.<locals>.one_step_on_data(data) should not modify its Python input arguments. Modifying a copy is allowed. The following parameter(s) were modified: data`
    `features` is modified with `pop`

    ```diff
    - labels = features.pop("user_rating")
    + copied_features = features.copy()
    + labels = copied_features.pop("user_rating")
    ```
1. `ValueError: could not convert string to float: 'M*A*S*H (1970)'`

    ```diff

      test_ratings[movie_title] = model({
    -     "user_id": np.array(["42"]),
    -     "movie_title": np.array([movie_title])
    +     "user_id": tf.convert_to_tensor(["42"]),
    +     "movie_title": tf.convert_to_tensor([movie_title])
      })
    ```
1. `TypeError: this __dict__ descriptor does not support '_DictWrapper' objects` in `tf.saved_model.save(model, "export")`
    This is Python 3.12 specific issue and workaround is `WRAPT_DISABLE_EXTENSIONS=1 poetry run python tensorflow/examples/movielens/rank.py`
    https://github.com/tensorflow/tensorflow/issues/63548

## Ref

1. [How to Install Google Scalable Nearest Neighbors (ScaNN) on Mac](https://eugeneyan.com/writing/how-to-install-scann-on-mac/)
1. [Efficient serving](https://www.tensorflow.org/recommenders/examples/efficient_serving)
