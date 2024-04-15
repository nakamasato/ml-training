# flask app

## Prepare

1. Install `river` and `flask`.

    ```
    poetry install
    ```

## How to use

1. Run flask app.

    ```
    FLASK_DEBUG=1 FLASK_APP=river/examples/flask-app/sample/app.py poetry run flask run
    ```

1. Send POST request. (train a model)

    ```
    curl -X POST http://localhost:5000/ -H "Content-Type: application/json" -d @river/examples/flask-app/sample/train-data.json
    ```

1. Send GET request. (predict)

    ```
    curl -X GET http://localhost:5000/ -H "Content-Type: application/json" -d @river/examples/flask-app/sample/predict-data.json
    {
    "false": 0.5,
    "true": 0.5
    }
    ```

## Reference

-
