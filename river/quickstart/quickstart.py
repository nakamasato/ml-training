from river import datasets
from river import compose
from river import linear_model
from river import metrics
from river import preprocessing


def check_datasets(dataset):
    for x, y in dataset:
        print(x)
        print(y)
        break


def model_example(dataset):
    """Use LR to predict phishing
    """

    model = compose.Pipeline(
        preprocessing.StandardScaler(),
        linear_model.LogisticRegression()
    )

    roc_auc = metrics.ROCAUC()

    for i, (x, y) in enumerate(dataset):
        y_pred = model.predict_proba_one(x)      # make a prediction
        roc_auc = roc_auc.update(y, y_pred)
        model = model.learn_one(x, y)      # make the model learn
        if i % 100 == 0:
            print(i, y_pred, roc_auc)


def main():
    dataset = datasets.Phishing()
    print("==== check datasets ====")
    check_datasets(dataset)

    print("==== model example ====")
    model_example(dataset)


if __name__ == '__main__':
    main()
