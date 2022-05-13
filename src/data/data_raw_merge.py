import json
import pathlib
import click
from typing import List

import pandas as pd


CONFIG_PATH = "metadata/download_config.json"

COLUMNS = {
    "network_countrycode": "Countrycode",
    "network_localid": "AirQualityNetwork",
    "network_namespace": "Namespace",
    "pollutant": "AirPollutant",
    "samplingpoint_localid": "SamplingPoint",
    "station_code": "AirQualityStationEoICode",
    "value_verification": "Verification",
    "value_validity": "Validity",
    "value_datetime_begin": "DatetimeBegin",
    "value_datetime_end": "DatetimeEnd",
    "value_numeric": "Concentration",
}


@click.command()
@click.argument("input_path", type=click.Path(), nargs=2)
@click.argument("output_path", type=click.Path())
def merge_eea_data(input_path: List[str], output_path: str):
    """
    This function concatenates historical and last updated datasets
    :param input_path: list of path with input data
    :param output_path: path to save file
    """
    file = pathlib.Path(output_path)
    if file.is_file():
        path = output_path
    else:
        path = input_path[0]

    input_file = pathlib.Path(input_path[1])
    if input_file.is_file():
        updated_data = pd.read_csv(
            input_path[1], index_col=False, encoding="latin1"
        ).rename(COLUMNS, axis="columns")
    else:
        updated_data = pd.read_csv(
            input_path[0], index_col=False)
        updated_data["Datetime"] = pd.to_datetime(updated_data["DatetimeEnd"])
        updated_data.to_csv(output_path, index=False)
        return

    historical_data = pd.read_csv(path, index_col=False)

    assert len(historical_data["AirQualityStationEoICode"].unique()) == 1
    assert len(historical_data["UnitOfMeasurement"].unique()) == 1

    with open(CONFIG_PATH) as json_file:
        config = json.load(json_file)
    code = config["AirQualityStationEoICode"]

    updated_data["UnitOfMeasurement"] = historical_data[
        "UnitOfMeasurement"
    ].unique()[0]

    data_new = pd.concat(
        [
            historical_data,
            updated_data.query("AirQualityStationEoICode == @code"),
        ],
        axis=0,
        join="inner",
    )

    data_new["DatetimeBegin"] = data_new["DatetimeBegin"].apply(
        lambda x: x.replace(" +", "+")
    )
    data_new["DatetimeEnd"] = data_new["DatetimeEnd"].apply(
        lambda x: x.replace(" +", "+")
    )
    data_new["Datetime"] = pd.to_datetime(data_new["DatetimeEnd"])
    data_new = data_new.drop_duplicates().sort_values("Datetime")

    data_new.to_csv(output_path, index=False)


if __name__ == "__main__":
    merge_eea_data()
