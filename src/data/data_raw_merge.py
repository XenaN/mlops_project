import os
import pathlib
import json
from datetime import date

import pandas as pd


INTERIM_UPDATED_EEA_PATH = '../../data/interim/updated_data_eea/'
RAW_HISTORICAL_EEA_PATH = '../../data/raw/historical_data_eea/'
RAW_UPDATED_EEA_PATH = '../../data/raw/updated_data_eea/'
METADATA_PATH = '../../metadata/download_tags.json'
CONFIG_PATH = '../../metadata/download_config.json'

COLUMNS = {'network_countrycode': 'Countrycode',
           'network_localid': 'AirQualityNetwork',
           'network_namespace': 'Namespace',
           'pollutant': 'AirPollutant',
           'samplingpoint_localid': 'SamplingPoint',
           'station_code': 'AirQualityStationEoICode',
           'value_unit': 'UnitOfMeasurement',
           'value_verification': 'Verification',
           'value_validity': 'Validity',
           'value_datetime_begin': 'DatetimeBegin',
           'value_datetime_end': 'DatetimeEnd',
           'value_numeric': 'Concentration'}


def merge_eea_data(country: str, pollutant: str, metadata_path: str, config_path: str):
    """
    This function concatenates historical and last updated datasets
    :param country: tag of country
    :param pollutant: tag of pollutant
    :param metadata_path: path with metadata
    :param config_path: configuration file
    """
    date_today = date.today().strftime("%Y%m%d")
    with open(metadata_path) as json_file:
        metadata = json.load(json_file)

    with open(config_path) as json_file:
        config = json.load(json_file)

    pathlib.Path(INTERIM_UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)
    if len(os.listdir(INTERIM_UPDATED_EEA_PATH)) == 0:
        path = f"{RAW_HISTORICAL_EEA_PATH}{country}_{pollutant}/"
    else:
        path = INTERIM_UPDATED_EEA_PATH

    list_csv = os.listdir(path)
    file_name = f"{RAW_UPDATED_EEA_PATH}{country}_{metadata[pollutant]}_{date_today}.csv"
    updated_data = pd.read_csv(file_name,
                               index_col=False,
                               encoding='latin1').rename(COLUMNS, axis='columns')

    for file in list_csv:
        historical_data = pd.read_csv(f"{path}{file}", index_col=False, encoding='latin1')

        code = config['AirQualityStationEoICode']
        assert len(historical_data['AirQualityStationEoICode'].unique()) == 1

        if historical_data['AirQualityStationEoICode'].unique()[0] == code:

            data_new = pd.concat([
                historical_data,
                updated_data.query("AirQualityStationEoICode == @code").sort_values("DatetimeEnd")
            ], axis=0, join="inner")

            data_new['DatetimeBegin'] = data_new['DatetimeBegin'].apply(lambda x: x.replace(" +", "+"))
            data_new['DatetimeEnd'] = data_new['DatetimeEnd'].apply(lambda x: x.replace(" +", "+"))
            data_new = data_new.drop_duplicates()

            data_new.to_csv(f"{INTERIM_UPDATED_EEA_PATH}{file}", index=False)


if __name__ == "__main__":
    metadata_temp = {
        "countries":
            ["ES"],
        "pollutants":
            ["CO"]
    }

    pathlib.Path(INTERIM_UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)

    for one_country in metadata_temp["countries"]:
        for one_pollutant in metadata_temp["pollutants"]:
            merge_eea_data(country=one_country,
                           pollutant=one_pollutant,
                           metadata_path=METADATA_PATH,
                           config_path=CONFIG_PATH)


