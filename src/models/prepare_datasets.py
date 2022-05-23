import click
from typing import List

import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), nargs=2)
def prepare_dataset(n_days: int, input_path: str, output_path: List[str]):
    """

    :param n_days:
    :param input_path:
    :param output_path:
    :return:
    """
    df = pd.read_csv(input_path,
                     parse_dates=['Datetime'],
                     index_col=['Datetime'])

    df_daily = df.resample('D').mean().interpolate()

    df_shifted = pd.concat([df_daily["AQI"].shift(1), df_daily["AQI"]],
                           axis=1).dropna()
    df_shifted.columns = ['AQI', 'AQI_t+1']

    train, test = df_shifted.iloc[:-1], df_shifted.tail(n_days)

    train.to_csv(output_path[0], index=False)
    test.to_csv(output_path[1], index=False)


if __name__ == "__main__":
    prepare_dataset()