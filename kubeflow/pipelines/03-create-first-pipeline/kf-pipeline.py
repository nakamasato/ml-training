import kfp
import kfp.components as comp


def merge_csv(file_path: comp.InputPath('Tarball'),  # noqa: F821
              output_csv: comp.OutputPath('CSV')):   # noqa: F821
    import glob
    import pandas as pd
    import tarfile

    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    df = pd.concat(
        [pd.read_csv(csv_file, header=None)
            for csv_file in glob.glob('data/*.csv')])
    df.to_csv(output_csv, index=False, header=False)


create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    output_component_file='component.yaml',  # This is optional. It saves the component spec for future use.
    base_image='python:3.9',
    packages_to_install=['pandas==1.1.4'])

web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/web/Download/component.yaml')


# Define a pipeline and create a task from a component:
def my_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    _ = create_step_merge_csv(file=web_downloader_task.outputs['data'])  # merge_csv_task
    # The outputs of the merge_csv_task can be referenced using the
    # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']


client = kfp.Client(host="http://localhost:8080")  # change arguments accordingly


# kfp.compiler.Compiler().compile(
#     pipeline_func=my_pipeline,
#     package_path='pipeline.yaml')
# client.upload_pipeline(
#     pipeline_package_path='pipeline.yaml',
#     pipeline_name='sample pipeline'
# )

client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={
        'url': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    }
)
