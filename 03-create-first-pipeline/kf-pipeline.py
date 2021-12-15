import kfp
import kfp.components as comp


import glob
import pandas as pd
import tarfile
import urllib.request


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

def merge_csv(file_path: comp.InputPath('Tarball'),
              output_csv: comp.OutputPath('CSV')):
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
    output_component_file='component.yaml', # This is optional. It saves the component spec for future use.
    base_image='python:3.9',
    packages_to_install=['pandas==1.1.4'])

web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/web/Download/component.yaml')

# Define a pipeline and create a task from a component:
def my_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    merge_csv_task = create_step_merge_csv(file=web_downloader_task.outputs['data'])
    # The outputs of the merge_csv_task can be referenced using the
    # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']

kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml')


client = kfp.Client(host="http://localhost:8080") # change arguments accordingly

client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={
        'url': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    })
