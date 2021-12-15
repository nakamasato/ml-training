# Run tutorial pipelines

1. Open Tutorial Pipelines.
    ![](pipelines.png)
1. Click on `Create run` button at right-top corner.
    ![](tutorial-pipeline.png)
    When creating run, the pipeline will schedule `Pod` in the `kubeflow` namespace.

    ```bash
    kubectl get po -n kubeflow | grep my-test-pipeline
    my-test-pipeline-beta-4xxvm-3208546888                              0/2     Completed   0          11m
    my-test-pipeline-beta-4xxvm-824297336                               0/2     Completed   0          12m
    ```

1. Check `runs`.
    ![](tutorial-pipeline-run.png)
1. Try running all other pipelines in the same way.
