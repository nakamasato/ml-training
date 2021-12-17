# Create first pipeline

## Prerequisite

- kubeflow pipelines (if not please check [01-setup-kubeflow-pipelines-in-local](../01-setup-kubeflow-pipelines-in-local))

## Pipeline

Make a simple pipeline of the following function.

```python
def download_and_merge_csv(url: str, output_csv: str):
    with urllib.request.urlopen(url) as res:
        tarfile.open(fileobj=res, mode="r|gz").extractall('data')
    df = pd.concat(
        [pd.read_csv(csv_file, header=None)
        for csv_file in glob.glob('data/*.csv')])
    df.to_csv(output_csv, index=False, header=False)
download_and_merge_csv(
    url='https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz',
    output_csv='merged_data.csv')
```

## 1. Install `kfp`

```
pip install kfp --upgrade
```

For more details: [Kubeflow Pipelines SDK API](https://kubeflow-pipelines.readthedocs.io/en/latest/index.html)

## 2. Prepare script `kf-pipeline.py`

1. Two components created with sdk `kfp.components`
    1. `web_downloader_op` with `load_component_from_url`
        ```python
        web_downloader_op = kfp.components.load_component_from_url(
        'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/web/Download/component.yaml')
        ```
    1. `create_step_merge_csv` with `create_component_from_func` with pipeline_func `merge_csv`
        ```python
        create_step_merge_csv = kfp.components.create_component_from_func(
            func=merge_csv,
            output_component_file='component.yaml', # This is optional. It saves the component spec for future use.
            base_image='python:3.9',
            packages_to_install=['pandas==1.1.4'])
        ```

1. Create a function for the pipeline.

    ```python
    def my_pipeline(url):
        web_downloader_task = web_downloader_op(url=url) # first component
        merge_csv_task = create_step_merge_csv(file=web_downloader_task.outputs['data']) # second component
    ```
1. Create kubeflow pipelines client.
    ```python
    client = kfp.Client(host="http://localhost:8080")
    ```
    Specify the kubeflow pipelines host.

1. Create and run the defined pipeline with `create_run_from_pipeline_func`
    ```python
    client.create_run_from_pipeline_func(
        my_pipeline,
        arguments={
            'url': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
        })
    ```

## 3. Run the script

Run the script

```bash
python kf-pipeline.py
```

Check pods

```bash
kubectl get po -n kubeflow
NAME                                              READY   STATUS      RESTARTS   AGE
cache-deployer-deployment-d95f8b79f-w4w9v         1/1     Running     0          34m
cache-server-55897df854-jllh7                     1/1     Running     0          34m
metadata-envoy-deployment-5b587ff9d4-zvq6b        1/1     Running     0          34m
metadata-grpc-deployment-6b5685488-g9gxs          1/1     Running     6          34m
metadata-writer-5c84d65485-t8zjj                  1/1     Running     1          34m
minio-5b65df66c9-p428b                            1/1     Running     0          34m
ml-pipeline-69c679bf86-fr7xz                      1/1     Running     6          34m
ml-pipeline-persistenceagent-69bdb89cfc-8tgnf     1/1     Running     1          34m
ml-pipeline-scheduledworkflow-f45d59698-9pl42     1/1     Running     0          34m
ml-pipeline-ui-78c69869b8-pmqcb                   1/1     Running     0          34m
ml-pipeline-viewer-crd-6d4dc67b48-96b67           1/1     Running     0          34m
ml-pipeline-visualizationserver-75d8c8cd9-8w4gh   1/1     Running     0          34m
my-pipeline-p2wzm-2262628660                      0/2     Completed   0          24m
my-pipeline-p2wzm-2680998630                      0/2     Completed   0          24m
mysql-f7b9b7dd4-748xh                             1/1     Running     0          34m
workflow-controller-99b6487-45xlx                 1/1     Running     0          34m
```

Check on UI

![](kfp-first-pipeline.png)


# Reference

- [Build a Pipeline](https://www.kubeflow.org/docs/components/pipelines/sdk/build-pipeline/)
