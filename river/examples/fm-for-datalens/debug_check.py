from river import datasets
from river import metrics
from river.evaluate import progressive_val_score

from river import optim
from river import compose
from river import facto
from river import optim
from river import stats


def evaluate(model):
    X_y = datasets.MovieLens100K()
    metric = metrics.MAE() + metrics.RMSE()
    _ = progressive_val_score(X_y, model, metric, print_every=25_000, show_time=True, show_memory=True)


def debug(model):
    for x, _ in datasets.MovieLens100K():
        report = model.debug_one(x)
        print(report)
        break


def split_genres(x):
    genres = x['genres'].split(', ')
    return {f'genre_{genre}': 1 / len(genres) for genre in genres}


def bin_age(x):
    if x['age'] <= 18:
        return {'age_0-18': 1}
    elif x['age'] <= 32:
        return {'age_19-32': 1}
    elif x['age'] < 55:
        return {'age_33-54': 1}
    else:
        return {'age_55-100': 1}


def debug_fm():
    fm_params = {
        'n_factors': 10,
        'weight_optimizer': optim.SGD(0.025),
        'latent_optimizer': optim.SGD(0.05),
        'sample_normalization': False,
        'l1_weight': 0.,
        'l2_weight': 0.,
        'l1_latent': 0.,
        'l2_latent': 0.,
        'intercept': 3,
        'intercept_lr': .01,
        'weight_initializer': optim.initializers.Zeros(),
        'latent_initializer': optim.initializers.Normal(mu=0., sigma=0.1, seed=73),
    }

    regressor = compose.Select('user', 'item')
    regressor += (
        compose.Select('genres') |
        compose.FuncTransformer(split_genres)
    )
    regressor += (
        compose.Select('age') |
        compose.FuncTransformer(bin_age)
    )
    regressor |= facto.FMRegressor(**fm_params)
    evaluate(regressor)
    debug(regressor)


def debug_ffm():
    dataset = (
        ({'user': 'Alice', 'item': 'Superman', 'time': .12}, 8),
        ({'user': 'Alice', 'item': 'Terminator', 'time': .13}, 9),
        ({'user': 'Alice', 'item': 'Star Wars', 'time': .14}, 8),
        ({'user': 'Alice', 'item': 'Notting Hill', 'time': .15}, 2),
        ({'user': 'Alice', 'item': 'Harry Potter ', 'time': .16}, 5),
        ({'user': 'Bob', 'item': 'Superman', 'time': .13}, 8),
        ({'user': 'Bob', 'item': 'Terminator', 'time': .12}, 9),
        ({'user': 'Bob', 'item': 'Star Wars', 'time': .16}, 8),
        ({'user': 'Bob', 'item': 'Notting Hill', 'time': .10}, 2)
    )
    model = facto.FFMRegressor(
        n_factors=10,
        intercept=5,
        seed=42,
    )

    for x, y in dataset:
        model = model.learn_one(x, y)

    print(model.predict_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14}))
    print(model.debug_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14}))


def debug_fwfm():
    dataset = (
        ({'user': 'Alice', 'item': 'Superman'}, 8),
        ({'user': 'Alice', 'item': 'Terminator'}, 9),
        ({'user': 'Alice', 'item': 'Star Wars'}, 8),
        ({'user': 'Alice', 'item': 'Notting Hill'}, 2),
        ({'user': 'Alice', 'item': 'Harry Potter '}, 5),
        ({'user': 'Bob', 'item': 'Superman'}, 8),
        ({'user': 'Bob', 'item': 'Terminator'}, 9),
        ({'user': 'Bob', 'item': 'Star Wars',}, 8),
        ({'user': 'Bob', 'item': 'Notting Hill'}, 2)
    )
    model = facto.FwFMRegressor(
        n_factors=10,
        intercept=5,
        seed=42,
    )

    for x, y in dataset:
        model = model.learn_one(x, y)

    print(model.predict_one({'Bob': 1, 'Harry Potter': 1}))
    print(model.debug_one({'Bob': 1, 'Harry Potter': 1}))


def debug_hofm():
    dataset = (
        ({'user': 'Alice', 'item': 'Superman', 'time': .12}, 8),
        ({'user': 'Alice', 'item': 'Terminator', 'time': .13}, 9),
        ({'user': 'Alice', 'item': 'Star Wars', 'time': .14}, 8),
        ({'user': 'Alice', 'item': 'Notting Hill', 'time': .15}, 2),
        ({'user': 'Alice', 'item': 'Harry Potter ', 'time': .16}, 5),
        ({'user': 'Bob', 'item': 'Superman', 'time': .13}, 8),
        ({'user': 'Bob', 'item': 'Terminator', 'time': .12}, 9),
        ({'user': 'Bob', 'item': 'Star Wars', 'time': .16}, 8),
        ({'user': 'Bob', 'item': 'Notting Hill', 'time': .10}, 2)
    )
    model = facto.HOFMRegressor(
        degree=3,
        n_factors=10,
        intercept=5,
        seed=42,
    )

    for x, y in dataset:
        _ = model.learn_one(x, y)

    print(model.predict_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14}))
    print(model.debug_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14}))

if __name__ == '__main__':
    debug_hofm()
