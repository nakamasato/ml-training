# [KServe](https://kserve.github.io/website/master/)

Highly scalable and standards based Model Inference Platform on Kubernetes for Trusted AI

## Architecture

![](https://github.com/kserve/website/blob/main/docs/images/controlplane.png?raw=true)
## Components

- [Istio](https://istio.io/): Simplify observability, traffic management, security, and policy with the leading service mesh.
- [Knative](https://knative.dev/docs/): *Kubernetes-based platform to deploy and manage modern serverless workloads.*
- [KServe](https://kserve.github.io/): *Highly scalable and standards based Model Inference Platform on Kubernetes for Trusted AI*
- [Cert Manager](https://cert-manager.io/docs/): *cert-manager adds certificates and certificate issuers as resource types in Kubernetes clusters, and simplifies the process of obtaining, renewing and using those certificates.*

## Deployment mode

1. `Serverless`: <- QuickStart
1. `RawDeployment`:
1. `ModelMeshDeployment`: designed for high-scale, high-density and frequently-changing model use cases

Default DeploymentMode is set in configmap

```
kubectl get configmap -n kserve inferenceservice-config -o jsonpath='{.data.deploy}'
{
  "defaultDeploymentMode": "Serverless"
}
```

### 1. Serverless

### 2. RawDeployment

### 3. ModelMeshDeployment (alpha)

1. [modelmesh-serving](https://github.com/kserve/modelmesh-serving)
1. [modelmesh](https://github.com/kserve/modelmesh)

![](https://github.com/kserve/website/blob/main/docs/images/ModelMesh-Serving.png?raw=true)

Solves the scalability problem:
1. Overhead resource due to the sidecars injected into each pod
1. Maximum number of pods per node
1. Each pod in `InferenceService` requires an independent IP


## [Getting Started](https://kserve.github.io/website/master/get_started/)

1. Prepare a Kubernetes cluster.
    If you run in local, please use Kubernetes in Docker Desktop (or minikube. I just confirmed with Docker Desktop). (Couldn't find a way to connect to `LoadBalancer` type `Service` from the host machine for `kind` cluster unless we use `NodePort` instead.)
1. Install `cert-manager`, `istio`, `knative`, `kserve`.

    ```
    curl -s "https://raw.githubusercontent.com/kserve/kserve/release-0.7/hack/quick_install.sh" | bash
    ```

    The script installs:

    1. Istio: 1.10.3
        ```
        curl -L https://git.io/getLatestIstio | sh -
        cd istio-${ISTIO_VERSION}
        ```

        Install IstioOperator in `istio-system` namespace with `istioctl`
    1. KNatve: v0.23.2
        Install CRDs, core, and, release.
    1. Cert Manager: v1.3.0
    1. KServe: v0.7.0

    ※ Might fail installation. Ususally rerunning the script would succeed. Might be caused by [x509 certificate related errors](https://istio.io/latest/docs/ops/common-problems/injection/#x509-certificate-related-errors), in that case, we need to restart `istiod` Pod.

    <details><summary>pods</summary>

    ```
    kubectl get pod -A
    NAMESPACE            NAME                                         READY   STATUS    RESTARTS   AGE
    cert-manager         cert-manager-76b7c557d5-rnkgx                1/1     Running   0          3m39s
    cert-manager         cert-manager-cainjector-655d695d74-gxvzn     1/1     Running   0          3m39s
    cert-manager         cert-manager-webhook-7955b9bb97-mj89j        1/1     Running   0          3m39s
    istio-system         istio-egressgateway-5547fcc8fc-4f5lx         1/1     Running   0          4m5s
    istio-system         istio-ingressgateway-8f568d595-9h9kj         1/1     Running   0          4m5s
    istio-system         istiod-568d797f55-dxs89                      1/1     Running   0          4m23s
    knative-serving      activator-7c4fbc97cf-c7jd8                   1/1     Running   0          3m44s
    knative-serving      autoscaler-87c6f49c-zsmpc                    1/1     Running   0          3m44s
    knative-serving      controller-78d6897c65-chqzl                  1/1     Running   0          3m44s
    knative-serving      istio-webhook-7b4d84887c-85tc9               1/1     Running   0          3m42s
    knative-serving      networking-istio-595947b649-x9jrh            1/1     Running   0          3m42s
    knative-serving      webhook-6bcf6c6658-qhlj8                     1/1     Running   0          3m44s
    kserve               kserve-controller-manager-0                  2/2     Running   0          2m49s
    kube-system          coredns-558bd4d5db-6f6nv                     1/1     Running   2          13d
    kube-system          coredns-558bd4d5db-l7csh                     1/1     Running   2          13d
    kube-system          etcd-kind-control-plane                      1/1     Running   2          13d
    kube-system          kindnet-vfxnf                                1/1     Running   2          13d
    kube-system          kube-apiserver-kind-control-plane            1/1     Running   2          13d
    kube-system          kube-controller-manager-kind-control-plane   1/1     Running   2          13d
    kube-system          kube-proxy-ph9fg                             1/1     Running   2          13d
    kube-system          kube-scheduler-kind-control-plane            1/1     Running   2          13d
    local-path-storage   local-path-provisioner-547f784dff-5t42j      1/1     Running   3          13d
    ```

    </details>


    <details><summary>If cluster doesn't support LoadBalancer</summary>

    Change istio-ingressgateway service type if you're running in the Kubernetes cluster that doesn't support LoadBalancer.

    https://qiita.com/chataro0/items/b01d1aa697666406e9ba#istio

    </details>

1. Check ingress gateway. (`EXTERNAL-IP` is `localhost`)

    ```
    kubectl get svc istio-ingressgateway -n istio-system
    NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                                                                      AGE
    istio-ingressgateway   LoadBalancer   10.101.34.67   localhost     15021:30144/TCP,80:30440/TCP,443:30663/TCP,31400:31501/TCP,15443:32341/TCP   73s
    ```

    ※ Might encounter [Kubernetes Load balanced services are sometimes marked as "Pending"](https://github.com/docker/for-mac/issues/4903) issue. The only way seems to be reset Kubernetes and restart Docker process.

1. Create test `InferenceService`.

    `sklearn-inference-service.yaml`:

    ```yaml
    apiVersion: "serving.kserve.io/v1beta1"
    kind: "InferenceService"
    metadata:
      name: "sklearn-iris"
    spec:
      predictor:
        sklearn:
          storageUri: "gs://kfserving-samples/models/sklearn/iris"
    ```

    ```
    kubectl create ns kserve-test
    kubectl apply -f sklearn-inference-service.yaml -n kserve-test
    ```

    wait a min

    ```
    kubectl get inferenceservices sklearn-iris -n kserve-test
    NAME           URL                                           READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                    AGE
    sklearn-iris   http://sklearn-iris.kserve-test.example.com   True           100                              sklearn-iris-predictor-default-00001   2m26s
    ```


1. Check with `iris-input.json`

    ```json
    {
      "instances": [
        [6.8,  2.8,  4.8,  1.4],
        [6.0,  3.4,  4.5,  1.6]
      ]
    }
    ```

    ```
    # export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    export INGRESS_HOST=localhost # if you're using docker-desktop
    export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
    ```

    ```
    SERVICE_HOSTNAME=$(kubectl get inferenceservice sklearn-iris -n kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)
    ```

    ```
    curl  -H "Host: ${SERVICE_HOSTNAME}" http://$INGRESS_HOST:$INGRESS_PORT/v1/models/sklearn-iris:predict -d @./data/iris-input.json

    {"predictions": [1, 1]}%
    ```

1. Performance test

    ```
    kubectl create -f https://raw.githubusercontent.com/kserve/kserve/release-0.7/docs/samples/v1beta1/sklearn/v1/perf.yaml -n kserve-test
    ```

    ```
    kubectl logs load-testvbfqw-hfbqj -n kserve-test
    Requests      [total, rate, throughput]         30000, 500.02, 500.00
    Duration      [total, attack, wait]             1m0s, 59.998s, 2.104ms
    Latencies     [min, mean, 50, 90, 95, 99, max]  1.837ms, 3.261ms, 2.819ms, 4.162ms, 5.264ms, 12.196ms, 49.735ms
    Bytes In      [total, mean]                     690000, 23.00
    Bytes Out     [total, mean]                     2460000, 82.00
    Success       [ratio]                           100.00%
    Status Codes  [code:count]                      200:30000
    Error Set:
    ```

1. Visualize by `kiali`

    [Prometheus](https://istio.io/latest/docs/ops/integrations/prometheus/)

    ```
    kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.12/samples/addons/prometheus.yaml
    ```

    [kiali](https://istio.io/latest/docs/ops/integrations/kiali/#installation)

    ```
    kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.12/samples/addons/kiali.yaml
    ```

    ```
    bin/istioctl dashboard kiali
    ```

    ![](docs/kiali.png)

1. Cleanup

    ```
    export ISTIO_VERSION=1.10.3
    export KNATIVE_VERSION=v0.23.2
    export KSERVE_VERSION=v0.7.0
    export CERT_MANAGER_VERSION=v1.3.0
    ```

    Delete KServce

    ```
    kubectl delete -f https://github.com/kserve/kserve/releases/download/$KSERVE_VERSION/kserve.yaml
    ```

    Delete cert-manager

    ```
    kubectl delete -f https://github.com/jetstack/cert-manager/releases/download/$CERT_MANAGER_VERSION/cert-manager.yaml
    ```

    Delete Knative

    ```
    kubectl delete --filename https://github.com/knative/serving/releases/download/$KNATIVE_VERSION/serving-crds.yaml
    kubectl delete --filename https://github.com/knative/serving/releases/download/$KNATIVE_VERSION/serving-core.yaml
    kubectl delete --filename https://github.com/knative/net-istio/releases/download/$KNATIVE_VERSION/release.yaml
    ```

    Delete istio if `istioctl` exists

    ```
    bin/istioctl manifest generate --set profile=demo | kubectl delete --ignore-not-found=true -f -
    kubectl delete namespace istio-system
    ```

## Implementation

### [InferenceServiceReconciler](https://github.com/kserve/kserve/blob/master/pkg/controller/v1beta1/inferenceservice/controller.go)

1. Fetch `InferenceService`
1. Filter by annotation
1. Skip reconcilation for `ModelMeshDeployment` mode.
1. Finalizer logic (add finalizer if not exists & deleteExternalResources if being deleted)
1. Add **predictors** (required), **transformers** (optional), and **explainers** (optional) to `reconciler`.
1. Call `Reconcile` for all the reconcilers set above.
1. Reconcile ingress.
    1. `RawDeployment` -> `NewRawIngressReconciler`
    1. `Serveless` -> `NewIngressReconciler`
1. Reconcile modelConfig.

Interesting point is InferenceServiceReconciler's reconcile function calls the [reconcile function](https://github.com/kserve/kserve/blob/master/pkg/controller/v1alpha1/trainedmodel/reconcilers/modelconfig/modelconfig_reconciler.go) of another controller.


### [Create your own model and SKLearn Server Locally](https://github.com/kserve/kserve/tree/master/docs/samples/v1beta1/sklearn/v1)

1. Create model.

    ```python
    from sklearn import svm
    from sklearn import datasets
    from joblib import dump
    clf = svm.SVC(gamma='scale')
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    clf.fit(X, y)
    dump(clf, 'model.joblib')
    ```

    ```
    python create_model.py
    ```

    -> `model.joblib`

1. Install sklearn-server following [Scikit-Learn Server](https://github.com/kserve/kserve/blob/master/python/sklearnserver/README.md)

    ```
    git clone https://github.com/kserve/kserve.git
    cd kserve/python/kserve
    ```

    https://github.com/kserve/kserve/tree/master/python/kserve

    ```
    pip install -e .
    ```

    ```
    cd - && cd kserve/python/sklearnserver
    ```

    ```
    pip install -e .
    ```
1. Run SKLearn Server

    ```
    python -m sklearnserver --model_dir ./  --model_name svm
    [I 220129 09:23:24 model_server:150] Registering model: svm
    [I 220129 09:23:24 model_server:123] Listening on port 8080
    [I 220129 09:23:24 model_server:125] Will fork 1 workers
    ```

1. Send a request from a client.

    ```
    python check_sklearn_server.py
    <Response [200]>
    {"predictions": [0]}
    ```

## References
- [KFServing](https://www.kubeflow.org/docs/components/kfserving/)
- [https://github.com/kserve/kserve](https://github.com/kserve/kserve)
- [Kubernetes で始める ML 基盤ハンズオン / ML Platform Hands-on with Kubernetes](https://speakerdeck.com/zuiurs/ml-platform-hands-on-with-kubernetes)
- [KServe: The next generation of KFServing](https://blog.kubeflow.org/release/official/2021/09/27/kfserving-transition.html)
- [environment setup](https://kserve.github.io/website/0.7/get_started/#install-the-kserve-quickstart-environment)
- [First InferenceService](https://kserve.github.io/website/0.7/get_started/first_isvc/#4-curl-the-inferenceservice)
- [kiali installation](https://istio.io/latest/docs/ops/integrations/kiali/#installation)
