import argparse

from ray.air import ScalingConfig, session
from ray.train.tensorflow import TensorflowTrainer
from ray.train.torch import TorchTrainer

import ray


def train_func(config):
    # train_dataset = session.get_dataset_shard("train")
    for i in range(config["num_epochs"]):
        session.report({"epoch": i})


def main(backend):
    train_dataset = ray.data.from_items([{"x": x, "y": 2 * x + 1} for x in range(200)])

    trainer = (
        TensorflowTrainer(
            train_func,
            train_loop_config={"num_epochs": 2},
            scaling_config=ScalingConfig(num_workers=2, use_gpu=False),
            datasets={"train": train_dataset},
        )
        if backend == "tensorflow"
        else TorchTrainer(
            train_func,
            train_loop_config={"num_epochs": 2},
            scaling_config=ScalingConfig(num_workers=2, use_gpu=False),
            datasets={"train": train_dataset},
        )
    )

    result = trainer.fit()
    print(result.metrics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend",
        "-b",
        required=True,
        type=str,
        help="Ray trainer backend either tensorflow or torch",
    )

    args, _ = parser.parse_known_args()
    main(args.backend)
