from river import compose, datasets, linear_model, metrics, preprocessing


def check_datasets(dataset):
    for x, y in dataset:
        print(x)
        print(y)
        break


def model_example(dataset):
    """Use LR to predict phishing"""

    model = compose.Pipeline(
        preprocessing.StandardScaler(), linear_model.LogisticRegression()
    )

    metric = metrics.ROCAUC()

    for i, (x, y) in enumerate(dataset):
        y_pred = model.predict_proba_one(x)  # make a prediction
        model.learn_one(x, y)  # make the model learn
        metric.update(y, y_pred)
        if i % 100 == 0:
            print(i, y_pred, metric)


def main():
    dataset = datasets.Phishing()
    print("==== check datasets ====")
    check_datasets(dataset)

    print("==== model example ====")
    model_example(dataset)


if __name__ == "__main__":
    main()
