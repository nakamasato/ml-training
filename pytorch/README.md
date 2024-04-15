# Pytorch

## version

torch: [1.13.1](https://github.com/pytorch/pytorch/releases/tag/v1.13.1)

## Prepare

```
poetry install
```

## Run

```
poetry run python pytorch/distributed_example.py
```

## CNN

Input x Filter (kernel) -> Feature Map (Overlapping application)

- Filter: The filter is smaller than the input data and the type of multiplication applied between a filter-sized patch of the input and the filter is a dot product. (will be learned by SGD to minimize the classification accuracy) Filter can capture feature. -> Multiple filters
- Feature Map: low-level features
- Multiple channels: color (red, green and blue). filter needs to have the same number of channels. 3x3 filter for 3 channles -> 3x3x3 (3-d)
- Multiple layers: extract features that are combination of lower-level features.

- https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-from-scratch-for-mnist-handwritten-digit-classification/
- [convolutional layer](https://machinelearningmastery.com/convolutional-layers-for-deep-learning-neural-networks/)


## References

- [Neural Networks](https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html#define-the-network)
- [train_dist.py](https://github.com/seba-1511/dist_tuto.pth/blob/gh-pages/train_dist.py)
- [Pytorch distributed overview](https://pytorch.org/tutorials/beginner/dist_overview.html)


## Error

<details><summary>No module named '_lzma'</summary>

```
Traceback (most recent call last):
  File "/Users/nakamasato/repos/nakamasato/ml-training/pytorch/distributed_example.py", line 4, in <module>
    import lzma
  File "/Users/nakamasato/.pyenv/versions/3.9.0/lib/python3.9/lzma.py", line 27, in <module>
    from _lzma import *
ModuleNotFoundError: No module named '_lzma'
```

```
brew install xz
```

</details>
