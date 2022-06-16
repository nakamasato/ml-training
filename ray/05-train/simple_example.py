import argparse

from ray.train import Trainer


def train_func(config):
    results = []
    for i in range(config["num_epochs"]):
        results.append(i)
    return results


def main(backend):
    trainer = Trainer(backend=backend, num_workers=2)
    trainer.start()
    print(trainer.run(train_func, config={"num_epochs": 2}))
    # [[0, 1], [0, 1]]
    print(trainer.run(train_func, config={"num_epochs": 5}))
    # [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
    trainer.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend", '-b', required=True, type=str, help="Ray trainer backend either tensorflow or torch"
    )

    args, _ = parser.parse_known_args()
    main(args.backend)
