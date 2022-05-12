import requests
import json
import click
from typing import Tuple
from multiprocessing import Pool
from itertools import product
import pathlib

import pandas as pd


SERVICE_URL = "http://discomap.eea.europa.eu/map/fme/latest"
HISTORICAL_EEA_PATH = "data/raw/historical_data_eea/"
UPDATED_EEA_PATH = "../../data/raw/updated_data_eea/"
TAGS_PATH = "metadata/download_tags.json"
METADATA_PATH = "metadata/download_config.json"


def download_urls_historical_data_from_discomap(
    country: str, pollutant: str, year_start: int, year_end: int
):
    """
    Save urls with historical data from discomap.eea.europa.eu
    :param country: tag of country
    :param pollutant: tag of pollutant
    :param year_start: Year_from parameter
    :param year_end: Year_to parameter
    """
    with open(TAGS_PATH) as json_file:
        metadata = json.load(json_file)

    with open(
        f"{HISTORICAL_EEA_PATH}{country}_{pollutant}_urls.txt", "wb"
    ) as urls_file:

        download_file = (
            f"https://fme.discomap.eea.europa.eu/fmedatastreaming/"
            f"AirQualityDownload/AQData_Extract.fmw?CountryCode={country}&City"
            f"Name=&Pollutant={metadata[pollutant]}&Year_from={year_start}"
            f"&Year_to={year_end}&Station=&Samplingpoint=&"
            f"Source=All&Output=TEXT&UpdateDate=&TimeCoverage=Year"
        )
        try:
            status = requests.get(download_file).status_code
            if status < 300:
                files = requests.get(download_file).content
                urls_file.write(files)
            else:
                print(f"Request has status code {status}")
        except Exception:
            print("Write fail")


def save_csv_from_url(pair_path_and_url: Tuple):
    """
    Pandas reads and saves dataframe from url
    :param pair_path_and_url: 0 - path to save data and 1 - url for dataset
    """
    try:
        dataset = pd.read_csv(pair_path_and_url[1], index_col=False)
        dataset.to_csv(
            f"{pair_path_and_url[0]}{pair_path_and_url[1].split('/')[-1]}",
            index=False
        )
    except Exception:
        print(f"Save csv file fail {pair_path_and_url[1]}")


@click.command()
@click.argument("pollutant", type=click.STRING)
@click.argument("n_cores", type=click.INT)
def download_historical_data_from_discomap_urls(pollutant: str, n_cores: int):
    """
    Save historical data from discomap.eea.europa.eu urls
    :param pollutant: tag of pollutant
    :param n_cores: number of cores
    """
    with open(METADATA_PATH) as json_file:
        metadata = json.load(json_file)

    download_urls_historical_data_from_discomap(
        metadata["country"],
        pollutant,
        metadata["year_start"],
        metadata["year_end"]
    )

    with open(
        f'{HISTORICAL_EEA_PATH}{metadata["country"]}_{pollutant}_urls.txt',
        "r",
        encoding="utf-8-sig",
    ) as file:
        urls = file.read().splitlines()

    country_pollutant_path = f"{HISTORICAL_EEA_PATH}/{metadata['country']}_" \
                             f"{pollutant}/"
    pathlib.Path(country_pollutant_path).mkdir(parents=True, exist_ok=True)

    with Pool(processes=n_cores) as pool:
        pool.map(save_csv_from_url, product([country_pollutant_path], urls))

    pathlib.Path(UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    pathlib.Path(HISTORICAL_EEA_PATH).mkdir(parents=True, exist_ok=True)
    download_historical_data_from_discomap_urls()
