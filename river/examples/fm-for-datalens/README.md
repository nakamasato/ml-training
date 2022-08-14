# FM

## Theory

1. Solve the following optimization problem:
    ```math
    \min_w \quad \frac{\lambda}{2} \quad || \bm{w} ||^2_2 + \sum_{i=1}^m{\log{(1+\exp{(-y_i \phi(\bm{w}, \bm{x}_i)))}}}
    ```
1. If we consider the linear model, it's difficult for the linear model to learn **feature conjunctions**.
    ```math
    \phi(\bm{w}, \bm{x}_i) = \bm{w} \cdot \bm{x}
    ```
1. Two approaches to address it:
    1. **degree-2 polynomial mappings (Poly2)**: (computational complexity: `O(n^2)`)
    1. **FMs (Factorization Machines)**: (computational complexity: `O(nk)`) <- better when dataset is ***sparse***
        1. PITF (Pairwise Interaction Tensor Factorization): consider special fields: `user`, `item` and `tag`
        1. Generalization of PITF "factor model" -> FFM (Field-aware Factorization Machines)
1. FM vs FFM:
    1. In **FMs**, every feature has only one latent vector to learn
the latent effect with any other features. -> ESPN is learned with `(w_espn, w_nike)` and `(w_espn, w_male)`. The latent effects of them might be different because `Nike` and `Male` belong to different fields.
        $$
        \bm{w}_{ESPN} \cdot \bm{w}_{Nike} + \bm{w}_{ESPN} \cdot \bm{w}_{Male} + \bm{w}_{Nike} \cdot \bm{w}_{Male}
        $$

        ```math
        \phi(\bm{w}, \bm{x}_i) = \sum_{j_{1}=1}^{n} \sum_{j_{2}=1}^{n} (\bm{w}_{j_{1}} \cdot \bm{w}_{j_{2}}) x_{j_{1}} x_{j_{2}}
        ```
    1. In **FFMs**, differentiate latent variable `W_ESPN` for `Gender` and `Advertiser`

        ```math
        \bm{w}_{ESPN, A} \cdot \bm{w}_{Nike, P} + \bm{w}_{ESPN, G} \cdot \bm{w}_{Male, P} + \bm{w}_{Nike, G} \cdot \bm{w}_{Male, A}
        ```

        ```math
        \phi(\bm{w}, \bm{x}_i) = \sum_{j_{1}=1}^{n} \sum_{j_{2}=1}^{n} (\bm{w}_{j_{1}, f_{2}} \cdot \bm{w}_{j_{2}, f_{1}}) x_{j_{1}} x_{j_{2}}
        ```

        -  `nfk` variables -> Computational complexity: `O(n^2k)`.
        - noting that each latent vector in FFMs only needs to learn the effect with a specific field:
            ```math
            k_{FFM} \ll k_{FM}
            ```
1. **SGD (Stochastic Gradient Descent)** for solving the optimization problem.
1. Summary for FFM:
    - FFMs should be effective for data sets that contain categorical features and are transformed to binary features.
    - If the transformed set is not sparse enough, FFMs seem to bring less benefit.
    - It is more difficult to apply FFMs on numerical data sets.
## Prepare

1. Create venv

    ```
    python3 -m venv venv
    ```

    ```
    source venv/bin/activate
    ```

1. Install `river`.

    ```
    pip install -r requirements.txt
    ```

## Run

```
python main.py
```

```python
x = {
    "user": "259",
    "item": "255",
    "timestamp": 874731910000000000,
    "title": "My Best Friend's Wedding (1997)",
    "release_date": 866764800000000000,
    "genres": "comedy, romance",
    "age": 21.0,
    "gender": "M",
    "occupation": "student",
    "zip_code": "48823"
}
y = 4.0
```

<details>

Result:

```bash
---- Naive prediction (Mean) ----
[25,000] MAE: 0.934259, RMSE: 1.124469
[50,000] MAE: 0.923893, RMSE: 1.105
[75,000] MAE: 0.937359, RMSE: 1.123696
[100,000] MAE: 0.942162, RMSE: 1.125783
---- Baseline Model ----
[25,000] MAE: 0.761844, RMSE: 0.960972 – 0:00:01.024150 – 169.99 KB
[50,000] MAE: 0.753292, RMSE: 0.951223 – 0:00:02.016820 – 238.63 KB
[75,000] MAE: 0.754177, RMSE: 0.953376 – 0:00:02.975559 – 282.43 KB
[100,000] MAE: 0.754651, RMSE: 0.954148 – 0:00:03.965410 – 306.03 KB
---- Funk Matrix Factorization ----
[25,000] MAE: 1.070136, RMSE: 1.397014 – 0:00:01.736032 – 938.07 KB
[50,000] MAE: 0.99174, RMSE: 1.290666 – 0:00:03.559525 – 1.13 MB
[75,000] MAE: 0.961072, RMSE: 1.250842 – 0:00:05.399589 – 1.33 MB
[100,000] MAE: 0.944883, RMSE: 1.227688 – 0:00:07.150453 – 1.5 MB
---- Biased Matrix Factorization ----
[25,000] MAE: 0.761818, RMSE: 0.961057 – 0:00:01.785283 – 1.01 MB
[50,000] MAE: 0.751667, RMSE: 0.949443 – 0:00:03.675949 – 1.28 MB
[75,000] MAE: 0.749653, RMSE: 0.948723 – 0:00:05.476340 – 1.51 MB
[100,000] MAE: 0.748559, RMSE: 0.947854 – 0:00:07.300822 – 1.69 MB
---- Mimic Biased Matrix Factorization ----
[25,000] MAE: 0.761761, RMSE: 0.960662 – 0:00:04.178081 – 1.16 MB
[50,000] MAE: 0.751922, RMSE: 0.949783 – 0:00:08.182062 – 1.36 MB
[75,000] MAE: 0.749822, RMSE: 0.948634 – 0:00:12.407454 – 1.58 MB
[100,000] MAE: 0.748393, RMSE: 0.94776 – 0:00:16.380310 – 1.77 MB
['item', 'user'] | FMRegressor
---- Matrix Factorization with improved features ----
[25,000] MAE: 0.760059, RMSE: 0.961415 – 0:00:10.340172 – 1.43 MB
[50,000] MAE: 0.751429, RMSE: 0.951504 – 0:00:20.680120 – 1.68 MB
[75,000] MAE: 0.750568, RMSE: 0.951592 – 0:00:31.184284 – 1.95 MB
[100,000] MAE: 0.75018, RMSE: 0.951622 – 0:00:41.458612 – 2.2 MB
---- Higher-Order Factorization Machines (HOFM) ----
[25,000] MAE: 0.761379, RMSE: 0.96214 – 0:00:34.140858 – 2.61 MB
[50,000] MAE: 0.751998, RMSE: 0.951589 – 0:01:07.865240 – 3.08 MB
[75,000] MAE: 0.750994, RMSE: 0.951616 – 0:01:41.710331 – 3.6 MB
[100,000] MAE: 0.750849, RMSE: 0.952142 – 0:02:15.464547 – 4.07 MB
---- Field-aware Factorization Machines (FFM) ----
[25,000] MAE: 0.758339, RMSE: 0.959047 – 0:00:14.922949 – 3.04 MB
[50,000] MAE: 0.749833, RMSE: 0.948531 – 0:00:29.939671 – 3.59 MB
[75,000] MAE: 0.749631, RMSE: 0.949418 – 0:00:44.886509 – 4.19 MB
[100,000] MAE: 0.749776, RMSE: 0.950131 – 0:00:59.894855 – 4.75 MB
---- Field-weighted Factorization Machines (FwFM) ----
[25,000] MAE: 0.761435, RMSE: 0.962211 – 0:00:20.229511 – 1.18 MB
[50,000] MAE: 0.754063, RMSE: 0.953248 – 0:00:40.263218 – 1.38 MB
[75,000] MAE: 0.754729, RMSE: 0.95507 – 0:01:00.275003 – 1.6 MB
[100,000] MAE: 0.755697, RMSE: 0.956542 – 0:01:20.338102 – 1.79 MB
---- Field-aware Factorization Machines (FFM) with 2_factor ----
[25,000] MAE: 0.761945, RMSE: 0.962218 – 0:00:09.476144 – 1.89 MB
[50,000] MAE: 0.752542, RMSE: 0.951308 – 0:00:18.907024 – 2.23 MB
[75,000] MAE: 0.75201, RMSE: 0.951857 – 0:00:28.388703 – 2.59 MB
[100,000] MAE: 0.752198, RMSE: 0.952571 – 0:00:37.778264 – 2.92 MB
---- Field-aware Factorization Machines (FFM) with 5_factor ----
[25,000] MAE: 0.758984, RMSE: 0.959729 – 0:00:12.245419 – 2.47 MB
[50,000] MAE: 0.750404, RMSE: 0.949119 – 0:00:24.452397 – 2.91 MB
[75,000] MAE: 0.750309, RMSE: 0.950067 – 0:00:36.550744 – 3.39 MB
[100,000] MAE: 0.750366, RMSE: 0.950646 – 0:00:48.707158 – 3.84 MB
---- Field-aware Factorization Machines (FFM) with 8_factor ----
[25,000] MAE: 0.758339, RMSE: 0.959047 – 0:00:15.174566 – 3.04 MB
[50,000] MAE: 0.749833, RMSE: 0.948531 – 0:00:30.579178 – 3.59 MB
[75,000] MAE: 0.749631, RMSE: 0.949418 – 0:00:45.818892 – 4.19 MB
[100,000] MAE: 0.749776, RMSE: 0.950131 – 0:01:01.164692 – 4.75 MB
---- Field-aware Factorization Machines (FFM) with 11_factor ----
[25,000] MAE: 0.758792, RMSE: 0.959463 – 0:00:19.054146 – 3.61 MB
[50,000] MAE: 0.750089, RMSE: 0.94876 – 0:00:37.950341 – 4.27 MB
[75,000] MAE: 0.749496, RMSE: 0.949241 – 0:00:57.520452 – 4.99 MB
[100,000] MAE: 0.749437, RMSE: 0.949802 – 0:01:15.349766 – 5.66 MB
---- Field-aware Factorization Machines (FFM) with 14_factor ----
[25,000] MAE: 0.757753, RMSE: 0.958563 – 0:00:20.302182 – 4.18 MB
[50,000] MAE: 0.749424, RMSE: 0.948214 – 0:00:43.559532 – 4.95 MB
[75,000] MAE: 0.749234, RMSE: 0.949015 – 0:01:04.635293 – 5.79 MB
[100,000] MAE: 0.749315, RMSE: 0.949727 – 0:01:26.410851 – 6.57 MB
---- Field-aware Factorization Machines (FFM) with 17_factor ----
[25,000] MAE: 0.757105, RMSE: 0.957786 – 0:00:23.174074 – 4.76 MB
[50,000] MAE: 0.748965, RMSE: 0.947776 – 0:00:46.113884 – 5.63 MB
[75,000] MAE: 0.748585, RMSE: 0.948412 – 0:01:08.320216 – 6.6 MB
[100,000] MAE: 0.748781, RMSE: 0.949217 – 0:01:30.476526 – 7.48 MB
```

</details>

## Models
### Mean

### Baseline

```math
\normalsize \hat{y}(x) = \bar{y} + bu_{u} + bi_{i}
```

```python
baseline_params = {
    'optimizer': optim.SGD(0.025),
    'l2': 0.,
    'initializer': optim.initializers.Zeros()
}

model = meta.PredClipper(
    regressor=reco.Baseline(**baseline_params),
    y_min=1,
    y_max=5
)
```

### Funk Matrix Factorization

```math
\normalsize \hat{y}(x) = \langle \textbf{v}_u, \textbf{v}_i \rangle
```

```python
funk_mf_params = {
    'n_factors': 10,
    'optimizer': optim.SGD(0.05),
    'l2': 0.1,
    'initializer': optim.initializers.Normal(mu=0., sigma=0.1, seed=73)
}

model = meta.PredClipper(
    regressor=reco.FunkMF(**funk_mf_params),
    y_min=1,
    y_max=5
)
```

### Biased MF

```math
\normalsize \hat{y}(x) = \bar{y} + bu_{u} + bi_{i} + \langle \textbf{v}_u, \textbf{v}_i \rangle \
```

### FM

```math
\normalsize \hat{y}(x) = w_{0} + \sum_{j=1}^{p} w_{j} x_{j} + \sum_{j=1}^{p} \sum_{j'=j+1}^{p} \langle \textbf{v}_j, \textbf{v}_{j'} \rangle x_{j} x_{j'}
```

```python
fm_params = {
    'n_factors': 10,
    'weight_optimizer': optim.SGD(0.025),
    'latent_optimizer': optim.SGD(0.05),
    'sample_normalization': False,
    'l1_weight': 0.,
    'l2_weight': 0.,
    'l1_latent': 0.,
    'l2_latent': 0.,
    'intercept': 3,
    'intercept_lr': .01,
    'weight_initializer': optim.initializers.Zeros(),
    'latent_initializer': optim.initializers.Normal(mu=0., sigma=0.1, seed=73),
}

regressor = compose.Select('user', 'item')
regressor |= facto.FMRegressor(**fm_params)

model = meta.PredClipper(
    regressor=regressor,
    y_min=1,
    y_max=5
)
```

You can check [###compose.Select](###compose.Select) in detail.

1. Specify which feature to use:

    ```python
    regressor = compose.Select('user', 'item')
    regressor
    Select (
    item
    user
    )
    ```
1. Finalize regressor with `facto.FMRegressor`

    ```python
    regressor |= facto.FMRegressor(**fm_params)
    ```

Internal implementation:

- **intercept**
    ```python
    self.intercept
    ```
- **weights**
    ```python
    [xi * self.weights.get(i, 0) for i, xi in x.items()]
    ```
- **latents**
    ```python
    sum(
        x[j1] * x[j2] * np.dot(self.latents[j1], self.latents[j2])
        for j1, j2 in itertools.combinations(x.keys(), 2)
    )
    ```
### HOFM

```math
\normalsize \hat{y}(x) = w_{0} + \sum_{j=1}^{p} w_{j} x_{j} + \sum_{l=2}^{d} \sum_{j_1=1}^{p} \cdots \sum_{j_l=j_{l-1}+1}^{p} \left(\prod_{j'=1}^{l} x_{j_{j'}} \right) \left(\sum_{f=1}^{k_l} \prod_{j'=1}^{l} v_{j_{j'}, f}^{(l)} \right)
```

```math
\normalsize \hat{y}(x) = w_{0} +
\sum_{j=1}^{p} w_{j} x_{j} +
\sum_{j^{\prime} > j} \langle \overline{\textbf{\textit{p}}}^{(2)}_j, \overline{\textbf{\textit{p}}}^{(2)}_{j^{\prime}} \rangle x_j x_{j^{\prime}} +
\sum_{j_3 > j_2 > j_1} \langle \overline{\textbf{\textit{p}}}^{(3)}_{j_1}, \overline{\textbf{\textit{p}}}^{(3)}_{j_2}, \overline{\textbf{\textit{p}}}^{(3)}_{j_3} \rangle x_{j_{1}} x_{j_{2}} x_{j_{3}} + ...

\sum_{j_m > ... > j_2 > j_1} \langle \overline{\textbf{\textit{p}}}^{(m)}_{j_1}, \overline{\textbf{\textit{p}}}^{(m)}_{j_2}, ..., \overline{\textbf{\textit{p}}}^{(m)}_{j_m} \rangle x_{j_{1}} x_{j_{2}} ... x_{j_{m}}
```

```math
\langle \overline{\textbf{\textit{p}}}^{(m)}_{j_1}, \overline{\textbf{\textit{p}}}^{(m)}_{j_2}, ..., \overline{\textbf{\textit{p}}}^{(m)}_{j_m} \rangle = sum(\overline{\textbf{\textit{p}}}^{(m)}_{j_1} \cdot \overline{\textbf{\textit{p}}}^{(m)}_{j_2} \cdot ... \cdot \overline{\textbf{\textit{p}}}^{(m)}_{j_m}) \quad \textrm{(sum of element-wise products)}
```

implementaion:

```python
    def _calculate_interactions(self, x):
        """Calculates greater than unary interactions."""
        return sum(
            self._calculate_interaction(x, d, combination)
            for d in range(2, self.degree + 1)
            for combination in itertools.combinations(x.keys(), d)
        )
        # combination is a tuple with `d` elements:
        # [combination for combination in itertools.combinations([1,2,3,4],2)] -> [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        # [combination for combination in itertools.combinations([1,2,3,4],3)] -> [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
```

For each combination, calculate the interaction:

```math
\textrm{ feature product } \quad x_{j_{2}} ... x_{j_{m}}
```

```math
\textrm{ latent scalar product } \quad \langle \overline{\textbf{\textit{p}}}^{(m)}_{j_1}, \overline{\textbf{\textit{p}}}^{(m)}_{j_2}, ..., \overline{\textbf{\textit{p}}}^{(m)}_{j_m} \rangle = sum(\overline{\textbf{\textit{p}}}^{(m)}_{j_1} \cdot \overline{\textbf{\textit{p}}}^{(m)}_{j_2} \cdot ... \cdot \overline{\textbf{\textit{p}}}^{(m)}_{j_m})
```

```python
    def _calculate_interaction(self, x, d, combination):
        feature_product = functools.reduce(
            lambda x, y: x * y, (x[j] for j in combination) # get feature value for each element of combination, and multiply them one by one.
            # >>> x = {1: 10, 2: 0.2, 3: 3}
            # >>> combination = (1,2,3)
            # >>> functools.reduce(lambda x, y: x * y, (x[j] for j in combination))
            # 6.0 (10*0.2*3)
        )
        latent_scalar_product = sum(
            functools.reduce(
                lambda x, y: x * y, (self.latents[j][d][f] for j in combination)
            )
            for f in range(self.n_factors)
        )
        # >>> combination = (1,2,3)
        # >>> n_factors = 3
        # >>> d = 3
        # >>> latents = {1: {3: [1,2,3]}, 2: {3: [10,20,30]}, 3: {3: [0.1, 0.2, 0.3]}}
        # >>> functools.reduce(lambda x, y: x * y, (latents[j][d][f] for j in combination))
        # 8.0
        # >>> sum(functools.reduce(lambda x, y: x * y, (latents[j][d][f] for j in combination)) for f in range(n_factors))
        # 36.0
        # >>> [1*10*0.1, 2*20*0.2, 3*30*0.3]
        # [1.0, 8.0, 27.0]
        # >>> sum([1*10*0.1, 2*20*0.2, 3*30*0.3])
        # 36.0
        return feature_product * latent_scalar_product
```

### FFM

```math
\normalsize \hat{y}(x) = w_{0} + \sum_{j=1}^{p} w_{j} x_{j} + \sum_{j=1}^{p} \sum_{j'=j+1}^{p} \langle \textbf{v}_{j, f_{j'}}, \textbf{v}_{j', f_{j}} \rangle x_{j} x_{j'}
```

```python
ffm_params = {
    'n_factors': 8,
    'weight_optimizer': optim.SGD(0.01),
    'latent_optimizer': optim.SGD(0.025),
    'intercept': 3,
    'latent_initializer': optim.initializers.Normal(mu=0., sigma=0.05, seed=73),
}

regressor = compose.Select('user', 'item')
regressor += (
    compose.Select('genres') |
    compose.FuncTransformer(split_genres)
)
regressor += (
    compose.Select('age') |
    compose.FuncTransformer(bin_age)
)
regressor |= facto.FFMRegressor(**ffm_params)

model = meta.PredClipper(
    regressor=regressor,
    y_min=1,
    y_max=5
)
```

Feature engineering:

```python
regressor
TransformerUnion (
  Select (
    item
    user
  ),
  Pipeline (
    Select (
      genres
    ),
    FuncTransformer (
      func="split_genres"
    )
  ),
  Pipeline (
    Select (
      age
    ),
    FuncTransformer (
      func="bin_age"
    )
  )
)
```

When to use FFM over FM:

> It is empirically proven that for large, sparse datasets with many categorical features, FFM performs better. Conversely, for small and dense datasets or numerical datasets, FFM may not be as effective as FM.
### Field-weighted Factorization Machines (FwFM)

```math
\normalsize \hat{y}(x) = w_{0} + \sum_{j=1}^{p} w_{j} x_{j} + \sum_{j=1}^{p} \sum_{j'=j+1}^{p} r_{f_j, f_{j'}} \langle \textbf{v}_j, \textbf{v}_{j'} \rangle x_{j} x_{j'}
```

## Implementation

### 1. Select features by [Select(base.Transformer)](https://github.com/online-ml/river/blob/main/river/compose/select.py#L65)

```python
from river import compose
x = {'a': 42, 'b': 12, 'c': 13} # features
compose.Select('c')
Select (
  c
)
compose.Select(('c', 'b'))
Select (
  ('c', 'b')
)
compose.Select('c').transform_one(x) # {'c': 13}
```

```python
from river import feature_extraction as fx
x = {'sales': 10, 'shop': 'Ikea', 'country': 'Sweden'}
pipeline = (compose.Select('sales') | fx.PolynomialExtender())
pipeline.transform_one(x) # {'sales': 10, 'sales*sales': 100}
```
### 2. Choose a model (regressor or classifier) e.g. FM

- `BiasedMF`, `FunkMF` -> `base.Recommender` -> `base.Regressor` -> `estimator.Estimator` -> `base.Base` & `abc.ABC`
- `FM`, `FFM`, `FwFM`, `HOFM` -> `BaseFM`
- `FMRegressor` -> `FM` & `base.Regressor)`: Factorization Machine for regression

### 3. Create a [Pipeline](https://github.com/online-ml/river/blob/82d48a6256496c557bb5ae0f95e0db19fa32c03a/river/compose/pipeline.py#L168) with [Estimators](https://github.com/online-ml/river/blob/82d48a6256496c557bb5ae0f95e0db19fa32c03a/river/base/estimator.py#L21-L27) (e.g. `Select`, `Regressor` ...)

```python
regressor = compose.Select('user', 'item') # compose.Select -> base.Transformer -> base.Estimator -> base.Base & abc.ABC
regressor |= facto.FMRegressor(**fm_params) # facto.FMRegressor -> ... -> estimator.Estimator ->
```

Meaning of `|=`: set the result of `__or__` function to the left hand variable.
- `facto.FMRegressor` -> -> `estimator.Estimator` has [`__or__`](https://github.com/online-ml/river/blob/82d48a6256496c557bb5ae0f95e0db19fa32c03a/river/base/estimator.py#L21-L27) and [`__ror__`](https://github.com/online-ml/river/blob/82d48a6256496c557bb5ae0f95e0db19fa32c03a/river/base/estimator.py#L29-L35)
- `__ror__`: `compose.Pipeline(other, self)`
- `__or__`: `compose.Pipeline(self, other)`
- [`compose.Pipeline`](https://github.com/online-ml/river/blob/82d48a6256496c557bb5ae0f95e0db19fa32c03a/river/compose/pipeline.py#L168): a pipeline of estimators. `Pipeline` -> `base.Estimator` -> `base.Base` & `abc.ABC`.
    - `compose.Pipeline.__init__(self, *steps)`: eventually using `union.TransformerUnion(self, other)` to add up multiple steps.
        ```python
        def __init__(self, *steps):
            self.steps = collections.OrderedDict()
            for step in steps:
                self |= step # defined in __or__
        ```
    - `__or__`:
        ```python
        def __or__(self, other):
            """Insert a step at the end of the pipeline."""
            self._add_step(other, at_start=False)
            return self
        ```
    - `__add__`:
        ```python
        def __add__(self, other):
            """Merge with another Pipeline or TransformerUnion into a TransformerUnion."""
            if isinstance(other, union.TransformerUnion):
                return other.__add__(self)
            return union.TransformerUnion(self, other)
        ```
- [`union.TransformerUnion()`](https://github.com/online-ml/river/blob/82d48a6256496c557bb5ae0f95e0db19fa32c03a/river/compose/union.py#L11) -> `base.Transformer`: Packs multiple transformers into a single one.
    - `__init__`:

        ```python
        def __init__(self, *transformers):
            self.transformers = {}
            for transformer in transformers:
                self += transformer
        ```
    - `__add__(self, other)`:
        ```python
        def __add__(self, other):
            return self._add_step(other)
        ```
    - `_add_step(self, transformer)`

        ```python
        def _add_step(self, transformer):
            """Adds a transformer while taking care of the input type."""

            name = None
            if isinstance(transformer, tuple):
                name, transformer = transformer

            # If the step is a function then wrap it in a FuncTransformer
            if isinstance(transformer, (types.FunctionType, types.LambdaType)):
                transformer = func.FuncTransformer(transformer)

            def infer_name(transformer):
                if isinstance(transformer, func.FuncTransformer):
                    return infer_name(transformer.func)
                elif isinstance(transformer, (types.FunctionType, types.LambdaType)):
                    return transformer.__name__
                elif hasattr(transformer, "__class__"):
                    return transformer.__class__.__name__
                return str(transformer)

            # Infer a name if none is given
            if name is None:
                name = infer_name(transformer)

            if name in self.transformers:
                counter = 1
                while f"{name}{counter}" in self.transformers:
                    counter += 1
                name = f"{name}{counter}"

            # Store the transformer
            self.transformers[name] = transformer

            return self
        ```
### 4. Wrap regressor with `meta.PredClipper` with y_min & y_max (deleted in [#741](https://github.com/online-ml/river/pull/741/files))

1. A model is defined by `meta.PredClipper()` with `regressor`

    ```python
    model = meta.PredClipper(
            regressor=reco.FunkMF(**funk_mf_params),
            y_min=1,
            y_max=5
        )
    ```
1. `PredClipper` -> `base.Regressor` & `base.WrapperMixin`
1. `learn_one` is just calling the `regressor.learn_one(x, y)`
1. [`predict_one`](https://github.com/online-ml/river/blob/8c9691855dd3c4a194d5818dac0df944d44ba9af/river/meta/pred_clipper.py#L64-L66) clips the prediction with `y_min` and `y_max`
    ```python
    def predict_one(self, x):
        y_pred = self.regressor.predict_one(x)
        return utils.math.clamp(y_pred, self.y_min, self.y_max)
    ```

### 5. Learn a model with a [Pipeline](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/compose/pipeline.py) (transformers + regressor/classifier/clusterer)

> Pipelines allow you to chain different steps into a sequence. Typically, when doing supervised learning, a pipeline contains one ore more transformation steps, whilst it's is a regressor or a classifier.

- Internal data:
    - `steps`: Ideally, a list of `(name, estimator)` tuples
- Example transformers:
    - [compose.Select](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/compose/select.py): select features to use.
    - [compose.FuncTransformer](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/compose/func.py): A function that update the feature dict `x`. e.g. parsing a date. `parse_date(x)` returns the updated `x` with a key `hour` with its value.
    - [feature_extraction.Agg](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/feature_extraction/agg.py)
- Usage:

    ```python
    scaler = preprocessing.StandardScaler()
    log_reg = linear_model.LinearRegression()
    model = scaler | log_reg
    ```
    - Ususally, we can use `|` to combine multiple estimators but you can also use `compose.Pipeline` constructor
    - `compose.TransformerUnion` can be used for complex pipelines
- Access to each step: same way as dictionary
    ```python
    model['LinearRegression']
    ```
- `debug_one`: You can visualize how the information flows and changes throughout the pipeline

    <details><summary>debug_one</summary>

    ```python
    >>> dataset = [
    ...     ('A positive comment', True),
    ...     ('A negative comment', False),
    ...     ('A happy comment', True),
    ...     ('A lovely comment', True),
    ...     ('A harsh comment', False)
    ... ]
    >>> tfidf = fx.TFIDF() | compose.Renamer(prefix='tfidf_')
    >>> counts = fx.BagOfWords() | compose.Renamer(prefix='count_')
    >>> mnb = naive_bayes.MultinomialNB()
    >>> model = (tfidf + counts) | mnb
    >>> for x, y in dataset:
    ...     model = model.learn_one(x, y)
    >>> x = dataset[0][0]
    >>> report = model.debug_one(dataset[0][0])
    >>> print(report)
    0. Input
    --------
    A positive comment
    <BLANKLINE>
    1. Transformer union
    --------------------
        1.0 TFIDF | Renamer
        -------------------
        tfidf_comment: 0.47606 (float)
        tfidf_positive: 0.87942 (float)
    <BLANKLINE>
        1.1 BagOfWords | Renamer
        ------------------------
        count_comment: 1 (int)
        count_positive: 1 (int)
    <BLANKLINE>
    count_comment: 1 (int)
    count_positive: 1 (int)
    tfidf_comment: 0.50854 (float)
    tfidf_positive: 0.86104 (float)
    <BLANKLINE>
    2. MultinomialNB
    ----------------
    False: 0.19313
    True: 0.80687
    ```

    </details>

- [learn_one](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/compose/pipeline.py#L299-L344): Learn with a series of transformations and an estimator.
    - For each steps:
        1. Run `t.transform_one`
        1. If the step is `TransformerUnion`, call `sub_t.learn_one` of sub transformers in the step (`t`)
        1. `t.learn_one`

    <details><summary>learn_one</summary>

    ```python
    def learn_one(self, x: dict, y=None, learn_unsupervised=False, **params):
        """Fit to a single instance.
        Parameters
        ----------
        x
            A dictionary of features.
        y
            A target value.
        learn_unsupervised
            Whether the unsupervised parts of the pipeline should be updated or not. See the
            docstring of this class for more information.
        """

        steps = iter(self.steps.values())

        # Loop over the first n - 1 steps, which should all be transformers
        for t in itertools.islice(steps, len(self.steps) - 1):
            x_pre = x
            x = t.transform_one(x=x)

            # The supervised transformers have to be updated.
            # Note that this is done after transforming in order to avoid target leakage.
            if isinstance(t, union.TransformerUnion):
                for sub_t in t.transformers.values():
                    if sub_t._supervised:
                        sub_t.learn_one(x=x_pre, y=y)
                    elif learn_unsupervised:
                        sub_t.learn_one(x=x_pre)

            elif t._supervised:
                t.learn_one(x=x_pre, y=y)

            elif learn_unsupervised:
                t.learn_one(x=x_pre)

        # At this point steps contains a single step, which is therefore the final step of the
        # pipeline
        final = next(steps)
        if final._supervised:
            final.learn_one(x=x, y=y, **params)
        elif learn_unsupervised:
            final.learn_one(x=x, **params)

        return self
    ```
    </details>

### 6. Evaluate with [progressive_val_score](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/evaluate/progressive_validation.py#L70) and [simulate_qa](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/stream/qa.py#L23-L110)

[`progressive_val_score`](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/evaluate/progressive_validation.py#L70): the canonical way to evaluate a model's performance

Usage example:

```python
def evaluate(model):
    X_y = datasets.MovieLens100K()
    metric = metrics.MAE() + metrics.RMSE()
    _ = progressive_val_score(X_y, model, metric, print_every=25_000, show_time=True, show_memory=True)
```

Set two metrics in the case above:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

```python
def progressive_val_score(
    dataset: base.typing.Dataset,
    model,
    metric: metrics.Metric,
    moment: typing.Union[str, typing.Callable] = None, # Timestamp for each observation. Can be a column name or callable function e.g. 'date' (a column name)
    delay: typing.Union[str, int, dt.timedelta, typing.Callable] = None, # How long is delayed before getting Y. It can be a callable function that calculates the delay. e.g. delay = lambda _, y: dt.timedelta(seconds=y)
    print_every=0,
    show_time=False,
    show_memory=False,
    **print_kwargs,
) -> metrics.Metric:
```

> Before updating the model with the pair (x, y), we can ask the model to predict the output of x, and thus obtain y-hat. We can then update a live metric by providing it with y and y-hat. Indeed, common metrics such as accuracy, MSE, and ROC AUC are all sums and can thus be updated online. By doing so, the model is trained with all the data in a single pass, and all the data is as well used as a validation set.

Steps in `progressive_val_score`:
1. Get the next sample.
1. Make a prediction.
1. Update a running average of the error.
1. Update the model.

If no delay is specified, it's same as the following:

```python
for x, y in datasets.Phishing():
    y_pred = model.predict_proba_one(x)
    metric = metric.update(y, y_pred)
    model = model.learn_one(x, y)
```

**Progressive validation** is too optimistic in that it can use the previous observation before the next observation prediction.

**Delayed progressive validation**

> If a model predicts the duration of a taxi trip, then obviously the duration of the trip, is only known once the taxi arrives at the desired destination. However, when using progressive validation, the model is given access to the true duration right after it has made a prediction. If the model is then asked to predict the duration of another trip which departs at a similar time as the previous trip, then it will be cheating because it knows how long the previous trip lasts.

> Instead of updating the model immediately after it has made a prediction, the idea is to update it once the ground truth would be available. This way the model learns and predicts samples without leakage.

Internally, this function calls [simulate_qa](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/stream/qa.py#L23-L110) function. The docstring is very helpful to gain in-depth underderstanding.

The logic produce events for the moment (the time observation without **y** comes in) and delayed time (when the **y** is made available.) is here:

<details><summary>main logic of simulate_qa</summary>

```python
for i, (x, y) in enumerate(dataset): # for each observation

    t = get_moment(i, x)
    d = get_delay(x, y)

    while mementos: # Stored observation as a tuple of four element (i, x, y, moment + delay) in a list.

        # Get the oldest answer
        i_old, x_old, y_old, t_expire = mementos[0]

        # If the oldest answer isn't old enough then stop
        if t_expire > t:
            break

        # Reveal the duration and pop the trip from the queue
        yield i_old, x_old, y_old
        del mementos[0]

    queue(mementos, Memento(i, x, y, t + d)) # Store each observation as a tuple of four element (i, x, y, moment, moment + delay) in a list
    if copy:
        x = deepcopy(x)
    yield i, x, None # for each observation just reveal i and x. Only when the delayed time has come, y is revealed.

for memento in mementos: # the remaining momentos are revealed after the for loop for dataset is done.
    yield memento.i, memento.x, memento.y
```

</details>

- Interestingly, when we generate dataset, if we wait until observation is complete and learn from the dataset, it might cause leakage or optimistic result.
    - example: impression (moment) ----> click or non-click (delayed)
    - If we wait for a while to determine the final observation for dataset, we need to **delay** for model assessment.


### 7. Predict (`transform_one(x)` for 1~n-1 `steps` + `final_step.predict_one(x)`)

The model, which is defined by a `Pipeline` above, predicts for a given `x`. A `Pipeline` usually consists of one or more transformers and a regression or a classifier. [predict_one](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/compose/pipeline.py#L390-L403) is very simple:
```python
def predict_one(self, x: dict, learn_unsupervised=True):
    x, final_step = self._transform_one(x=x, learn_unsupervised=learn_unsupervised)
    return final_step.predict_one(x=x)
```
1. Call `_transform_one` and get `x` (updated by all the transformers (1~n-1 steps)) and `final_step`.
    1. `_transform_one` method takes care of applying the **first n - 1 steps** of the pipeline. `transform_one` for each sub transformer for all the transformers (first n - 1 steps) are called and update `x`, while `learn_one` for each transformer ususally does nothing.

        <details><summary>details</summary>

        1. For each transformer
            1. In case transformer is `union.TransformerUnion`, for each sub transformer of the target transformer, call their `learn_one` if the condition `not _supervised and learn_unsupervised` is met.
            - Examples of `supervised` instance variable:
                - `True`: [Estimator (base class)](https://github.com/online-ml/river/blob/09a24d35c1f548239c54c1244973241bfe5c4edc/river/base/estimator.py#L11-L19) Regressor, Classifier, etc.
                - `False`: Transformer, Clusterer, etc.
            - `learn_one` for Transformer: A lot of transformers don't actually have to do anything during the `learn_one` step because they are stateless. For this reason **the default behavior of this function is to do nothing**.
            1. Call its `transform_one`.
                - `Transformer`s has their main logic in this function, while other estimators don't have `transform_one` method.
        </details>
    1. Call `learn_one` if `final_step` meets `not final_step._supervised and learn_unsupervised` this condition. (e.g. not called for regressor)
1. Return the result of `final_step`'s `predict_one(x)`.

### 8. Model

Where and how is the models is kept?
As you can see, a model is defined as a `Pipeline`, a series of steps, the last step of which is the actual estimator. The final step contains the model parameters.

## Reference

1. river docs
    1. https://riverml.xyz/latest/examples/matrix-factorization-for-recommender-systems-part-1/
    1. https://riverml.xyz/latest/examples/matrix-factorization-for-recommender-systems-part-2/
    1. https://riverml.xyz/latest/examples/matrix-factorization-for-recommender-systems-part-3/ (ToDo)
1. Evaluation
    1. ROC: [Receiver operating characteristic](https://www.wikiwand.com/en/Receiver_operating_characteristic)
    1. [The correct way to evaluate online machine learning models](https://maxhalford.github.io/blog/online-learning-evaluation/)
    1. [Using k-fold cross-validation for time-series model selection](https://stats.stackexchange.com/questions/14099/using-k-fold-cross-validation-for-time-series-model-selection)
    1. [Beating the Hold-Out: Bounds for K-fold and Progressive Cross-Validation](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.153.3925&rep=rep1&type=pdf)
    1. Progressive validation: [Ad Click Prediction: a View from the Trenches](https://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/41159.pdf)
1. Papers
    1. [Field-awareなFactorization Machinesの最新動向(2019)](https://qiita.com/guglilac/items/6c8971d27c143e2567a4)
    1. FM: [Factorization Machines](https://www.csie.ntu.edu.tw/~b97053/paper/Rendle2010FM.pdf)
    1. FFM: [Field-aware Factorization Machines for CTR Prediction](https://www.csie.ntu.edu.tw/~cjlin/papers/ffm.pdf)
    1. FwFM: [Field-weighted Factorization Machines for Click-Through Rate Prediction in Display Advertising](https://arxiv.org/pdf/1806.03514.pdf)
    1. HOFM: [Higher-Order Factorization Machines](https://proceedings.neurips.cc/paper/2016/file/158fc2ddd52ec2cf54d3c161f2dd6517-Paper.pdf)
    1. [On the Difficulty of Evaluating Baselines A Study on Recommender Systems](https://arxiv.org/pdf/1905.01395.pdf)
1. Blogs
    1. http://surpriselib.com/
    1. https://qiita.com/tohtsky/items/87239d4f6f8cd3c5f95f
