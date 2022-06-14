import pickle
from os.path import exists

from flask import Flask, request
from river import compose, linear_model, preprocessing

app = Flask(__name__)


@app.route('/', methods=['GET'])
def predict():
    payload = request.json
    river_model = load_model()
    return river_model.predict_proba_one(payload)


@app.route('/', methods=['POST'])
def learn():
    payload = request.json
    river_model = load_model()
    river_model.learn_one(payload['features'], payload['target'])
    save_model(river_model)
    return {}, 201


def new_model():
    model = compose.Pipeline(
        preprocessing.StandardScaler(),
        linear_model.LogisticRegression()
    )
    return model


def load_model():
    model_file = 'model.pkl'
    if exists(model_file):
        with open(model_file, 'rb') as f:
            return pickle.load(f)
    else:
        model = new_model()
        save_model(model)
        return model


def save_model(model):
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)


app.run(host='0.0.0.0', port=5000)
