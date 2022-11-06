# flask app

## Prepare

1. Create venv

    ```
    python3 -m venv venv
    ```

    ```
    source venv/bin/activate
    ```

1. Install `river` and `flask`.

    ```
    pip install -r requirements.txt
    ```

## How to use

1. Run flask app.

    ```
    cd sample
    FLASK_DEBUG=1 flask run
    ```

1. Send POST request. (train a model)

    ```
    curl -X POST http://localhost:5000/ -H "Content-Type: application/json" -d @examples/flask-app/sample/train-data.json
    ```

1. Send GET request. (predict)

    ```
    curl -X GET http://localhost:5000/ -H "Content-Type: application/json" -d @examples/flask-app/sample/predict-data.json
    {
    "false": 0.5,
    "true": 0.5
    }
    ```

## Reference

-
