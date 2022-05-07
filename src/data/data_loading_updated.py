import requests
import json
from datetime import date
import pathlib


SERVICE_URL = "http://discomap.eea.europa.eu/map/fme/latest"
METADATA_PATH = '../../metadata/download_tags.json'
UPDATED_EEA_PATH = '../../data/raw/updated_data_eea/'


def download_updated_data_from_discomap(country: str, pollutant: str):
    """
    Save from discomap.eea.europa.eu updated data
    :param country: tag of country
    :param pollutant: tag of pollutant
    """
    with open(METADATA_PATH) as json_file:
        metadata = json.load(json_file)

    date_today = date.today().strftime("%Y%m%d")

    file_name = f"{UPDATED_EEA_PATH}{country}_{metadata[pollutant]}_{date_today}.csv"
    download_file = f"{SERVICE_URL}/{country}_{pollutant}.csv"

    file = requests.get(download_file).content
    output = open(file_name, 'wb')
    output.write(file)
    output.close()


if __name__ == "__main__":
    with open('../../metadata/download_config.json') as json_file:
        metadata = json.load(json_file)

    pathlib.Path(UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)

    for one_pollutant in metadata["pollutants"]:
        download_updated_data_from_discomap(country=metadata["country"],
                                            pollutant=one_pollutant)
