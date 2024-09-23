# https://www.tensorflow.org/recommenders/examples/quickstart
# https://www.tensorflow.org/recommenders/examples/basic_retrieval
import tensorflow_recommenders as tfrs

from typing import Dict, Text
import google.cloud.logging
import tempfile
import logging
import os
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

IS_PRODUCTION = os.getenv("ENV", "dev") in ["prod", "production"]
if IS_PRODUCTION:
    client = google.cloud.logging.Client()
    client.setup_logging()
else:
    logging.basicConfig(level=logging.INFO)

# Env Var: https://cloud.google.com/vertex-ai/docs/training/code-requirements#environment-variables
MODEL_DIR = os.getenv("AIP_MODEL_DIR", tempfile.mkdtemp()) # you can write /gcs/<bucket>/<path> if you want to save the model to GCS
CHECKPOINT_DIR = os.path.join("AIP_CHECKPOINT_DIR", tempfile.mkdtemp())
TENSORBOARD_LOG_DIR = os.path.join("AIP_TENSORBOARD_LOG_DIR", tempfile.mkdtemp())

# Read data
ratings = tfds.load("movielens/100k-ratings", split="train")
# Features of all the available movies.
movies = tfds.load("movielens/100k-movies", split="train")

ratings = ratings.map(lambda x: {
    "movie_title": x["movie_title"],
    "user_id": x["user_id"]
})
movies = movies.map(lambda x: x["movie_title"]) # MapDataset で各ElementはTensor

user_ids_vocabulary = tf.keras.layers.StringLookup(mask_token=None) # mapping for known user_ids
user_ids_vocabulary.adapt(ratings.map(lambda x: x["user_id"]))

movie_titles_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
movie_titles_vocabulary.adapt(movies)


class MovieLensModel(tfrs.Model):
  # We derive from a custom base class to help reduce boilerplate. Under the hood,
  # these are still plain Keras Models.

  def __init__(
      self,
      user_model: tf.keras.Model,
      movie_model: tf.keras.Model,
      task: tfrs.tasks.Retrieval):
    super().__init__()

    # Set up user and movie representations.
    self.user_model = user_model
    self.movie_model = movie_model

    # Set up a retrieval task.
    self.task = task

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
    # Define how the loss is computed.

    user_embeddings = self.user_model(features["user_id"])
    movie_embeddings = self.movie_model(features["movie_title"])

    return self.task(user_embeddings, movie_embeddings)

# Define user (user_id) and movie (movie_title) models.
user_model = tf.keras.Sequential([
    user_ids_vocabulary, # user_id -> integer に変換
    tf.keras.layers.Embedding(user_ids_vocabulary.vocabulary_size(), 64) # integer -> embedding vector に変換
])
movie_model = tf.keras.Sequential([
    movie_titles_vocabulary,
    tf.keras.layers.Embedding(movie_titles_vocabulary.vocabulary_size(), 64)
])

# Define your objectives.
task = tfrs.tasks.Retrieval(metrics=tfrs.metrics.FactorizedTopK(
    movies.batch(128).map(movie_model)
  )
)

# Create a retrieval model.
model = MovieLensModel(user_model, movie_model, task)
model.compile(optimizer=tf.keras.optimizers.Adagrad(0.5))

# Train for 3 epochs.
model.fit(ratings.batch(4096), epochs=3)


# !pip install -q scann
is_scann = False
try:
  index = tfrs.layers.factorized_top_k.ScaNN(model.user_model)
  index.index_from_dataset(
    tf.data.Dataset.zip((movies.batch(100), movies.batch(100).map(model.movie_model)))
  )
  is_scann = True
except: # noqa E722
  # Use brute-force search to set up retrieval using the trained representations.
  index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
  index.index_from_dataset(
    movies.batch(100).map(lambda title: (title, model.movie_model(title))))


# Get recommendations.
_, titles = index(np.array(["42"]))
print(f"Top 3 recommendations for user 42: {titles[0, :3]}")


index.save(MODEL_DIR, options=tf.saved_model.SaveOptions(namespace_whitelist=["Scann"]) if is_scann else None)
print(f"Model saved to {MODEL_DIR}")
