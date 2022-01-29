# Kubeflow Training

## Prerequisite

- [kind](https://kind.sigs.k8s.io/)
    ```
    kind version
    kind v0.11.1 go1.16.4 darwin/amd64
    ```

### Create Kubernetes Cluster

Create local cluster

```
kind create cluster --config=kind-config.yaml
```

If ingress is necessary:

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## Contents

1. [Kubeflow Pipelines](pipelines)
1. [KServe](kserve)
