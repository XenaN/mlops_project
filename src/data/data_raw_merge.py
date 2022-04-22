import os

import pandas as pd


INTERIM_UPDATED_EEA_PATH = '../../data/interim/updated_data_eea/'
RAW_HISTORICAL_EEA_PATH = '../../data/raw/historical_data_eea/'
RAW_UPDATED_EEA_PATH = '../../data/raw/updated_data_eea/'

COLUMNS = {'network_countrycode': 'Countrycode',
           'network_localid': 'AirQualityNetwork',
           'network_namespace': 'Namespace',
           'pollutant': 'AirPollutant',
           'samplingpoint_localid': 'SamplingPoint',
           'value_unit': 'UnitOfMeasurement',
           'value_verification': 'Verification',
           'value_validity': 'Validity',
           'value_datetime_begin': 'DatetimeBegin',
           'value_datetime_end': 'DatetimeEnd',
           'value_numeric': 'Concentration'}


def merge_eea_data(filename: str):
    """
    This function concatenates historical and last updated datasets
    :param filename: filename for last updated data
    """
    updated_data = pd.read_csv(f"{RAW_UPDATED_EEA_PATH}{filename}",
                               index_col=False, encoding='latin1').rename(COLUMNS, axis='columns')
    if len(os.listdir(INTERIM_UPDATED_EEA_PATH)) == 0:
        list_csv = os.listdir(RAW_HISTORICAL_EEA_PATH)
        list_csv.remove('urls.txt')
        path = RAW_HISTORICAL_EEA_PATH
    else:
        list_csv = os.listdir(INTERIM_UPDATED_EEA_PATH)
        path = INTERIM_UPDATED_EEA_PATH

    for file in list_csv:
        historical_data = pd.read_csv(f"{path}{file}", index_col=False, encoding='latin1')

        assert len(historical_data['SamplingPoint'].unique()) == 1

        data_new = pd.concat([updated_data.query(f"SamplingPoint == {historical_data['SamplingPoint'].unique()}"),
                              historical_data], axis=0, join="inner")

        data_new['DatetimeBegin'] = data_new['DatetimeBegin'].apply(lambda x: x.replace(" +", "+"))
        data_new['DatetimeEnd'] = data_new['DatetimeEnd'].apply(lambda x: x.replace(" +", "+"))
        data_new = data_new.drop_duplicates()

        data_new.to_csv(f"{INTERIM_UPDATED_EEA_PATH}{file}", index=False)


if __name__ == "__main__":
    filename = 'ES_CO_20220422.csv'
    merge_eea_data(filename)


