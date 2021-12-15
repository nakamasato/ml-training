# Setup kubeflow pipelines in local

## Set up Kubernetes in local

There are several options to run Kubernetes cluster in local but here I use [kind](https://kind.sigs.k8s.io/)

1. Create kind cluster.
    ```bash
    kind create cluster # this will create a kind cluster named "kind"
    ```
1. Check all pods are running.
    ```bash
    kubectl get pod -A
    ```

## Deploy kubeflow pipelines

```bash
export PIPELINE_VERSION=1.7.1
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

Check

```bash
kubectl get pod -A
NAMESPACE            NAME                                              READY   STATUS      RESTARTS   AGE
kube-system          coredns-558bd4d5db-29hhg                          1/1     Running     0          27m
kube-system          coredns-558bd4d5db-sbz8q                          1/1     Running     0          27m
kube-system          etcd-kind-control-plane                           1/1     Running     0          27m
kube-system          kindnet-nmrzh                                     1/1     Running     0          27m
kube-system          kube-apiserver-kind-control-plane                 1/1     Running     0          27m
kube-system          kube-controller-manager-kind-control-plane        1/1     Running     0          27m
kube-system          kube-proxy-sf7b9                                  1/1     Running     0          27m
kube-system          kube-scheduler-kind-control-plane                 1/1     Running     0          27m
kubeflow             cache-deployer-deployment-d95f8b79f-w4w9v         1/1     Running     0          27m
kubeflow             cache-server-55897df854-jllh7                     1/1     Running     0          27m
kubeflow             metadata-envoy-deployment-5b587ff9d4-zvq6b        1/1     Running     0          27m
kubeflow             metadata-grpc-deployment-6b5685488-g9gxs          1/1     Running     6          27m
kubeflow             metadata-writer-5c84d65485-t8zjj                  1/1     Running     1          27m
kubeflow             minio-5b65df66c9-p428b                            1/1     Running     0          27m
kubeflow             mysql-f7b9b7dd4-748xh                             1/1     Running     0          27m
kubeflow             workflow-controller-99b6487-45xlx                 1/1     Running     0          27m
local-path-storage   local-path-provisioner-547f784dff-z6swz           1/1     Running     0          27m
```

You can check UI by

```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Open http://localhost:8080

![](kfp-ui.png)

# Reference

- https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/
