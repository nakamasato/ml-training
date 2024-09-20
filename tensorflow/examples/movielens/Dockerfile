FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# this is necessary ref: https://github.com/tensorflow/recommenders/issues/712
ENV TF_USE_LEGACY_KERAS=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY retrieve.py .

CMD ["python", "retrieve.py"]
