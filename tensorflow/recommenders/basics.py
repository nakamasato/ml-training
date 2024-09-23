

import tensorflow as tf
import tensorflow_datasets as tfds


# Features of all the available movies.
movies = tfds.load("movielens/100k-movies", split="train")

movie_titles = movies.map(lambda x: x["movie_title"])

movie_titles_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
movie_titles_vocabulary.adapt(movie_titles)


# 仮の映画モデル
class SimpleMovieModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        # StringLookup レイヤーを追加して、文字列を整数に変換
        self.string_lookup = movie_titles_vocabulary
        self.embedding = tf.keras.layers.Embedding(input_dim=movie_titles_vocabulary.vocabulary_size(), output_dim=32)

    def call(self, inputs):
        # 文字列の映画タイトルを整数IDに変換
        integer_ids = self.string_lookup(inputs["movie_title"])
        return self.embedding(integer_ids)

# モデルのインスタンスを作成
movie_model = SimpleMovieModel()

# バッチごとに映画モデルを適用
embedded_movies = movies.map(lambda x: movie_model(x))

# embedded_movies は、映画の埋め込みベクトルを含むデータセット
# for batch in embedded_movies:
#     print(batch)  # Embedding ベクトルを表示 tf.Tensor
