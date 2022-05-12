import os
import pathlib
import json
import click
from datetime import date

import pandas as pd


INTERIM_UPDATED_EEA_PATH = "data/interim/updated_data_eea/"
RAW_HISTORICAL_EEA_PATH = "data/raw/historical_data_eea/"
RAW_UPDATED_EEA_PATH = "data/raw/updated_data_eea/"
METADATA_PATH = "metadata/download_tags.json"
CONFIG_PATH = "metadata/download_config.json"

COLUMNS = {
    "network_countrycode": "Countrycode",
    "network_localid": "AirQualityNetwork",
    "network_namespace": "Namespace",
    "pollutant": "AirPollutant",
    "samplingpoint_localid": "SamplingPoint",
    "station_code": "AirQualityStationEoICode",
    "value_unit": "UnitOfMeasurement",
    "value_verification": "Verification",
    "value_validity": "Validity",
    "value_datetime_begin": "DatetimeBegin",
    "value_datetime_end": "DatetimeEnd",
    "value_numeric": "Concentration",
}


@click.command()
@click.argument("pollutant", type=click.STRING)
def merge_eea_data(pollutant: str):
    """
    This function concatenates historical and last updated datasets
    :param pollutant: tag of pollutant
    """
    date_today = date.today().strftime("%Y%m%d")
    with open(METADATA_PATH) as json_file:
        metadata = json.load(json_file)

    with open(CONFIG_PATH) as json_file:
        config = json.load(json_file)

    file_name = f"{RAW_UPDATED_EEA_PATH}{config['country']}_" \
                f"{metadata[pollutant]}_{date_today}.csv"

    if len(os.listdir(RAW_UPDATED_EEA_PATH)) == 0:
        print(f"{file_name} does not exist")
        return

    pathlib.Path(INTERIM_UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)
    if len(os.listdir(INTERIM_UPDATED_EEA_PATH)) == 0:
        path = f"{RAW_HISTORICAL_EEA_PATH}{config['country']}_{pollutant}/"
    else:
        path = INTERIM_UPDATED_EEA_PATH

    list_csv = os.listdir(path)
    updated_data = pd.read_csv(file_name,
                               index_col=False,
                               encoding="latin1").rename(
        COLUMNS, axis="columns"
    )

    for file in list_csv:
        historical_data = pd.read_csv(
            f"{path}{file}", index_col=False, encoding="latin1"
        )

        code = config["AirQualityStationEoICode"]
        assert len(historical_data["AirQualityStationEoICode"].unique()) == 1

        if historical_data["AirQualityStationEoICode"].unique()[0] == code:

            data_new = pd.concat(
                [
                    historical_data,
                    updated_data.query(
                        "AirQualityStationEoICode == @code").sort_values(
                        "DatetimeEnd"
                    )
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
            data_new = data_new.drop_duplicates()

            data_new.to_csv(
                f"{INTERIM_UPDATED_EEA_PATH}{config['country']}_"
                f"{pollutant}_historical_updated.csv",
                index=False,
            )


if __name__ == "__main__":
    pathlib.Path(INTERIM_UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)

    merge_eea_data()
