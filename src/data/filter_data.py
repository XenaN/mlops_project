import os
import click
import json
import pathlib

import pandas as pd


CONFIG_PATH = "metadata/download_config.json"


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def filter_data(input_path: str, output_path: str):
    """
    Choose station from config
    :param input_path: path with input data
    :param output_path: path to save file
    """
    with open(CONFIG_PATH) as json_file:
        config = json.load(json_file)

    list_csv = os.listdir(input_path)

    table_filtered = pd.DataFrame()
    for file in list_csv:
        historical_data = pd.read_csv(
            f"{input_path}{file}", index_col=False, encoding="latin1"
        )

        code = config["AirQualityStationEoICode"]
        assert len(historical_data["AirQualityStationEoICode"].unique()) == 1
        assert len(historical_data["UnitOfMeasurement"].unique()) == 1

        if historical_data["AirQualityStationEoICode"].unique()[0] == code:
            table_filtered = pd.concat([table_filtered, historical_data],
                                       axis=0)

    table_filtered.to_csv(output_path, index=False)


if __name__ == "__main__":
    filter_data()

