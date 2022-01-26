# [KServe](https://kserve.github.io/website/master/)

Model Inference Platform on Kubernetes

- [environment setup](https://kserve.github.io/website/0.7/get_started/#install-the-kserve-quickstart-environment)
- [First InferenceService](https://kserve.github.io/website/0.7/get_started/first_isvc/#4-curl-the-inferenceservice)

1. Create Kubernetes cluster with kind.
    ```
    kind create cluster
    ```
1. Install `cert-manager`, `istio`, `knative-serving`, `kserve`.

    ```
    curl -s "https://raw.githubusercontent.com/kserve/kserve/release-0.7/hack/quick_install.sh" | bash
    ```

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

    ```
    kubectl get svc istio-ingressgateway -n istio-system
    NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                                                                      AGE
    istio-ingressgateway   LoadBalancer   10.96.170.71   <pending>     15021:30529/TCP,80:32100/TCP,443:32120/TCP,31400:31644/TCP,15443:31203/TCP   10m
    ```

1. Check with `iris-input.json` (not yet)

```
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
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
