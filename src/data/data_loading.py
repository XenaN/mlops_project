import requests
import json
from typing import List
from datetime import date
from multiprocessing import Pool

import pandas as pd

SERVICE_URL = "http://discomap.eea.europa.eu/map/fme/latest"
HISTORICAL_EEA_PATH = '../../data/raw/historical_data_eea/'
METADATA_PATH = '../../metadata/download_tags.json'
UPDATED_EEA_PATH = '../../data/raw/updated_data_eea/'


def download_urls_historical_data_from_discomap(countries: List, pollutants: List,
                                                year_start: int, year_end: int):
    """
    Save urls with historical data from discomap.eea.europa.eu
    :param countries: list of countries
    :param pollutants: list of pollutant tags
    :param year_start: Year_from parameter
    :param year_end: Year_to parameter
    """
    with open(METADATA_PATH) as json_file:
        metadata = json.load(json_file)

    with open(f'{HISTORICAL_EEA_PATH}urls.txt', 'wb') as urls_file:
        for country in countries:
            for pollutant in pollutants:
                download_file = f"https://fme.discomap.eea.europa.eu/fmedatastreaming/" \
                                f"AirQualityDownload/AQData_Extract.fmw?CountryCode={country}&City" \
                                f"Name=&Pollutant={metadata[pollutant]}&Year_from={year_start}" \
                                f"&Year_to={year_end}&Station=&Samplingpoint=&" \
                                f"Source=All&Output=TEXT&UpdateDate=&TimeCoverage=Year"
                try:
                    files = requests.get(download_file).content
                    urls_file.write(files)
                except Exception:
                    print("Write fail")


def save_csv_from_url(url: str):
    """
    :param url: url for dataset
    """
    try:
        dataset = pd.read_csv(url, index_col=False)
        dataset.to_csv(f"{HISTORICAL_EEA_PATH}{url.split('/')[-1]}", index=False)
    except Exception:
        print("Save csv file fail")


def download_historical_data_from_discomap_urls(countries: List, pollutants: List,
                                                year_start: int, year_end: int):
    """
    Save historical data from discomap.eea.europa.eu urls
    :param countries: list of countries
    :param pollutants: list of pollutant tags
    :param year_start: Year_from parameterhttp://discomap.eea.europa.eu/
    :param year_end: Year_to parameter
    """
    download_urls_historical_data_from_discomap(countries, pollutants, year_start, year_end)

    with open(f'{HISTORICAL_EEA_PATH}urls.txt', 'r', encoding='utf-8-sig') as file:
        urls = file.readlines()

    with Pool(processes=8) as pool:
        pool.map(save_csv_from_url, urls)


def download_updated_data_from_discomap(countries: List, pollutants: List):
    """
    Save from discomap.eea.europa.eu updated data
    :param countries: list of countries
    :param pollutants: list of pollutant tags
    """
    for country in countries:
        for pollutant in pollutants:
            date_today = date.today().strftime("%Y%m%d")
            file_name = f"{UPDATED_EEA_PATH}{country}_{pollutant}_{date_today}.csv"
            download_file = f"{SERVICE_URL}/{country}_{pollutant}.csv"

            file = requests.get(download_file).content
            output = open(file_name, 'wb')
            output.write(file)
            output.close()


if __name__ == "__main__":
    metadata = {
        "countries":
            ["ES"],
        "pollutants":
            ["CO"],
        "year_start": 2022,
        "year_end": 2022
    }
    download_historical_data_from_discomap_urls(countries=metadata["countries"],
                                                pollutants=metadata["pollutants"],
                                                year_start=metadata["year_start"],
                                                year_end=metadata["year_end"])
    download_updated_data_from_discomap(countries=metadata["countries"],
                                        pollutants=metadata["pollutants"])

