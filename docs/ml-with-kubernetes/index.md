# Machine Learning with Kubernetes

## Overview

![](ml-with-kubernetes.drawio.svg)

## Steps

1. Deploy trainer
    1. Train batch (read data from storage e.g. GCS, S3, file with a prefix of objects)
    1. Start online training after completing batch training. (read data from queue e.g. Kafka, Kinesis, PubSub)
1. Predictor is a cache that stores model parameters

## Implementation

- the official Python client for kubernetes https://github.com/kubernetes-client/python
