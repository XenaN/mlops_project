import requests
import json
from typing import Tuple
from datetime import date
from multiprocessing import Pool
from itertools import product
import pathlib

import pandas as pd

SERVICE_URL = "http://discomap.eea.europa.eu/map/fme/latest"
HISTORICAL_EEA_PATH = '../../data/raw/historical_data_eea/'
METADATA_PATH = '../../metadata/download_tags.json'
UPDATED_EEA_PATH = '../../data/raw/updated_data_eea/'


def download_urls_historical_data_from_discomap(save_path: str, metadata_path: str,
                                                country: str, pollutant: str,
                                                year_start: int, year_end: int):
    """
    Save urls with historical data from discomap.eea.europa.eu
    :param save_path: path to save data
    :param metadata_path: path with metadata
    :param country: tag of country
    :param pollutant: tag of pollutant
    :param year_start: Year_from parameter
    :param year_end: Year_to parameter
    """
    with open(metadata_path) as json_file:
        metadata = json.load(json_file)

    with open(f'{save_path}{country}_{pollutant}_urls.txt', 'wb') as urls_file:

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


def save_csv_from_url(pair_path_and_url: Tuple):
    """
    Pandas reads and saves dataframe from url
    :param pair_path_and_url: 0 - path to save data and 1 - url for dataset
    """
    try:
        dataset = pd.read_csv(pair_path_and_url[1], index_col=False)
        dataset.to_csv(f"{pair_path_and_url[0]}{pair_path_and_url[1].split('/')[-1]}", index=False)
    except Exception:
        print("Save csv file fail")


def download_historical_data_from_discomap_urls(save_path: str, metadata_path: str,
                                                country: str, pollutant: str,
                                                year_start: int, year_end: int, n_cores: int):
    """
    Save historical data from discomap.eea.europa.eu urls
    :param save_path: path to save data
    :param metadata_path: path with metadata
    :param country: tag of country
    :param pollutant: tag of pollutant
    :param year_start: Year_from parameter
    :param year_end: Year_to parameter
    :param n_cores: number of cores
    """
    download_urls_historical_data_from_discomap(save_path, metadata_path,
                                                country, pollutant,
                                                year_start, year_end)

    with open(f'{save_path}{country}_{pollutant}_urls.txt', 'r', encoding='utf-8-sig') as file:
        urls = file.read().splitlines()

    country_pollutant_path = f"{save_path}/{country}_{pollutant}/"
    pathlib.Path(country_pollutant_path).mkdir(parents=True, exist_ok=True)

    with Pool(processes=n_cores) as pool:
        pool.map(save_csv_from_url, product([country_pollutant_path], urls))


def download_updated_data_from_discomap(save_path: str, metadata_path: str,
                                        url: str, country: str, pollutant: str):
    """
    Save from discomap.eea.europa.eu updated data
    :param save_path: path to save data
    :param metadata_path: path with metadata
    :param url: url with data
    :param country: tag of country
    :param pollutant: tag of pollutant
    """
    with open(metadata_path) as json_file:
        metadata = json.load(json_file)

    date_today = date.today().strftime("%Y%m%d")

    file_name = f"{save_path}{country}_{metadata[pollutant]}_{date_today}.csv"
    download_file = f"{url}/{country}_{pollutant}.csv"

    file = requests.get(download_file).content
    output = open(file_name, 'wb')
    output.write(file)
    output.close()


if __name__ == "__main__":
    metadata_temp = {
        "countries":
            ["ES"],
        "pollutants":
            ["CO"],
        "year_start": 2022,
        "year_end": 2022
    }

    pathlib.Path(HISTORICAL_EEA_PATH).mkdir(parents=True, exist_ok=True)
    pathlib.Path(UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)

    for one_country in metadata_temp["countries"]:
        for one_pollutant in metadata_temp["pollutants"]:
            download_historical_data_from_discomap_urls(save_path=HISTORICAL_EEA_PATH,
                                                        metadata_path=METADATA_PATH,
                                                        country=one_country,
                                                        pollutant=one_pollutant,
                                                        year_start=metadata_temp["year_start"],
                                                        year_end=metadata_temp["year_end"],
                                                        n_cores=8)
            download_updated_data_from_discomap(save_path=UPDATED_EEA_PATH,
                                                metadata_path=METADATA_PATH,
                                                url=SERVICE_URL,
                                                country=one_country,
                                                pollutant=one_pollutant)

