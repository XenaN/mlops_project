import click
from typing import List

import pandas as pd


@click.command()
@click.argument("depth", type=click.INT)
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), nargs=2)
def prepare_dataset(depth: int, input_path: str, output_path: List[str]):
    """
    Preparation datasets, daily resampling, choose column for features,
    split to train and test
    :param depth: number of day shift
    :param input_path: path of dataset
    :param output_path: path for saving train and test datasets
    """
    df = pd.read_csv(input_path, parse_dates=["Datetime"], index_col=["Datetime"])

    df_daily = df.resample("D").mean().interpolate()
    df_daily = df_daily.loc["2020-04-03 00:00:00+01:00":"2021-01-01 00:00:00+01:00"]

    columns = [x for x in df_daily.columns if "avg" in x]
    x_list = [df_daily[columns].shift(i) for i in range(1, depth + 1)]
    df_shifted = pd.concat([df_daily["AQI"]] + x_list, axis=1)
    df_shifted.columns = ["AQI"] + list(range(1, df_shifted.shape[1]))

    df_shifted = df_shifted.iloc[depth:]

    n_train = int(df_shifted.shape[0] * 0.77)
    train, test = df_shifted.iloc[:n_train], df_shifted.iloc[n_train:]

    train.to_csv(output_path[0], index=False)
    test.to_csv(output_path[1], index=False)


if __name__ == "__main__":
    prepare_dataset()
