# Quickstart

## Steps

1. Check python

    ```
    python -V
    Python 3.9.0
    ```

1. Create venv

    ```
    python3 -m venv venv
    ```

    ```
    source venv/bin/activate
    ```

1. Install `river`

    ```
    pip install -r requirements.txt
    ```

1. Run `main.py`

    ```
    python main.py
    ```

    ```
    {'age_of_domain': 1,
    'anchor_from_other_domain': 0.0,
    'empty_server_form_handler': 0.0,
    'https': 0.0,
    'ip_in_url': 1,
    'is_popular': 0.5,
    'long_url': 1.0,
    'popup_window': 0.0,
    'request_from_other_domain': 0.0}
    True
    ```

## Reference

https://github.com/online-ml/river
