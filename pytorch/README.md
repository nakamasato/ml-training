# Pytorch

version 1.11.0

Prepare:

```
python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run:

```
python distributed_example.py
```

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

```
pyenv uninstall 3.9.0
pyenv install 3.9.0
```
encountered error https://github.com/pyenv/pyenv/issues/2143

```
brew install pyenv # upgrade pyenv from 2.2.5 -> 2.3.1
```

```
pyenv install 3.9.0
```

</details>
