import requests
import json
import pathlib


SERVICE_URL = "http://discomap.eea.europa.eu/map/fme/latest"
UPDATED_EEA_PATH = "data/external/"


def download_updated_data_from_discomap(country: str, pollutant: str):
    """
    Save from discomap.eea.europa.eu updated data
    :param country: tag of country
    :param pollutant: tag of pollutant
    """
    file_name = f"{UPDATED_EEA_PATH}{country}_{pollutant}.csv"
    download_file = f"{SERVICE_URL}/{country}_{pollutant}.csv"

    status = requests.get(download_file).status_code
    if status < 300:
        file = requests.get(download_file).content
        output = open(file_name, "wb")
        output.write(file)
        output.close()
    else:
        print(f"Request has status code {status}")


if __name__ == "__main__":
    with open("metadata/download_config.json") as json_file:
        metadata = json.load(json_file)

    pathlib.Path(UPDATED_EEA_PATH).mkdir(parents=True, exist_ok=True)

    for one_pollutant in metadata["pollutants"]:
        download_updated_data_from_discomap(
            country=metadata["country"], pollutant=one_pollutant
        )
