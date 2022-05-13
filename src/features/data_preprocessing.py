import click
import json
from typing import List, Dict

import yaml
import numpy as np
import pandas as pd


METADATA_POLLUTANT_PATH = "metadata/metadata_pollutants.yaml"
CONFIG_PATH = "metadata/download_config.json"


def change_units(df: pd.DataFrame, metadata: Dict, unit: str):
    """
    This function changes mg/m**3 to ppm
    :param df: table
    :param metadata: molar mass info path
    :param unit: new unit
    """
    assert df["UnitOfMeasurement"].unique() == ["mg/m3"] or df[
        "UnitOfMeasurement"
    ].unique() == ["µg/m3"]
    assert len(df["AirPollutant"].unique()) == 1

    # The number 24.45 in the equations above is the volume (liters)
    # of a mole (gram molecular weight) of a gas or vapour when the
    # pressure is at 1 atmosphere and at 25°C.
    coefficient = 24.45
    k = 1
    if df["UnitOfMeasurement"].unique() == ["µg/m3"] and unit == "ppm":
        k = 0.001

    df["Concentration_correct"] = (
        df["Concentration"]
        * coefficient
        * k
        / metadata[df["AirPollutant"].unique()[0]]
    )


def get_subindex(I_low: int, I_hi: int, c_low: float, c_hi: float, c: float):
    """
    Common formula for calculation AQI for one pollutant
    :param I_low: AQI value corresponding to c_low
    :param I_hi: AQI value corresponding to c_hi
    :param c_low: concentration breakpoint that is less than c
    :param c_hi: concentration breakpoint that is less than c
    :param c: current contentration
    """
    return ((I_hi - I_low) / (c_hi - c_low)) * (c - c_low) + I_low


def get_CO_subindex(x: float):
    """
    Calculation AQI only for CO
    :param x: concentration value
    """
    if x <= 4.4:
        return get_subindex(I_low=0, I_hi=50, c_low=0, c_hi=4.4, c=x)
    elif x <= 9.4:
        return get_subindex(I_low=51, I_hi=100, c_low=4.5, c_hi=9.4, c=x)
    elif x <= 12.4:
        return get_subindex(I_low=101, I_hi=150, c_low=4.5, c_hi=12.4, c=x)
    elif x <= 15.4:
        return get_subindex(I_low=151, I_hi=200, c_low=12.5, c_hi=15.4, c=x)
    elif x <= 30.4:
        return get_subindex(I_low=201, I_hi=300, c_low=15.5, c_hi=30.4, c=x)
    elif x <= 40.4:
        return get_subindex(I_low=301, I_hi=400, c_low=30.5, c_hi=40.4, c=x)
    elif x <= 50.4:
        return get_subindex(I_low=401, I_hi=500, c_low=40.5, c_hi=50.4, c=x)
    elif x > 50.4:
        return np.Inf
    else:
        return None


def get_O3_subindex(x: float):
    """
    Calculation AQI only for O3
    :param x: concentration value
    """
    if x <= 0.054:
        return get_subindex(I_low=0, I_hi=50, c_low=0, c_hi=0.054, c=x)
    elif x <= 0.07:
        return get_subindex(I_low=51, I_hi=100, c_low=0.055, c_hi=0.07, c=x)
    elif x <= 0.085:
        return get_subindex(I_low=101, I_hi=150, c_low=0.071, c_hi=0.085, c=x)
    elif x <= 0.105:
        return get_subindex(I_low=151, I_hi=200, c_low=0.086, c_hi=0.105, c=x)
    elif x <= 0.200:
        return get_subindex(I_low=201, I_hi=300, c_low=0.106, c_hi=0.200, c=x)
    elif x > 0.200:
        return np.inf
    else:
        return None


def get_NO2_subindex(x: float):
    """
    Calculation AQI only for NO2
    :param x: concentration value
    """
    if x <= 53:
        return get_subindex(I_low=0, I_hi=50, c_low=0, c_hi=53, c=x)
    elif x <= 100:
        return get_subindex(I_low=51, I_hi=100, c_low=54, c_hi=100, c=x)
    elif x <= 360:
        return get_subindex(I_low=101, I_hi=150, c_low=101, c_hi=360, c=x)
    elif x <= 649:
        return get_subindex(I_low=151, I_hi=200, c_low=361, c_hi=649, c=x)
    elif x <= 1249:
        return get_subindex(I_low=201, I_hi=300, c_low=650, c_hi=1249, c=x)
    elif x <= 1649:
        return get_subindex(I_low=301, I_hi=400, c_low=1250, c_hi=1649, c=x)
    elif x <= 2049:
        return get_subindex(I_low=401, I_hi=500, c_low=1650, c_hi=2049, c=x)
    elif x > 2049:
        return np.Inf
    else:
        return None


def get_SO2_subindex(x: float):
    """
    Calculation AQI only for SO2
    :param x: concentration value
    """
    if x <= 35:
        return get_subindex(I_low=0, I_hi=50, c_low=0, c_hi=35, c=x)
    elif x <= 75:
        return get_subindex(I_low=51, I_hi=100, c_low=36, c_hi=75, c=x)
    elif x <= 185:
        return get_subindex(I_low=101, I_hi=150, c_low=76, c_hi=185, c=x)
    elif x <= 304:
        return get_subindex(I_low=151, I_hi=200, c_low=186, c_hi=304, c=x)
    elif x > 304:
        return np.Inf
    else:
        return None


def get_PM10_subindex(x: float):
    """
    Calculation AQI only for PM10
    :param x: concentration value
    """
    if x <= 54:
        return get_subindex(I_low=0, I_hi=50, c_low=0, c_hi=54, c=x)
    elif x <= 154:
        return get_subindex(I_low=51, I_hi=100, c_low=55, c_hi=154, c=x)
    elif x <= 254:
        return get_subindex(I_low=101, I_hi=150, c_low=155, c_hi=254, c=x)
    elif x <= 354:
        return get_subindex(I_low=151, I_hi=200, c_low=155, c_hi=354, c=x)
    elif x <= 424:
        return get_subindex(I_low=201, I_hi=300, c_low=355, c_hi=424, c=x)
    elif x <= 504:
        return get_subindex(I_low=301, I_hi=400, c_low=425, c_hi=504, c=x)
    elif x <= 604:
        return get_subindex(I_low=401, I_hi=500, c_low=505, c_hi=604, c=x)
    elif x > 604:
        return np.Inf
    else:
        return None


def getPM25_subindex(x: float):
    """
    Calculation AQI only for PM2.5
    :param x: concentration value
    """
    if x <= 12.0:
        return get_subindex(I_low=0, I_hi=50, c_low=0, c_hi=12.0, c=x)
    elif x <= 35.4:
        return get_subindex(I_low=51, I_hi=100, c_low=12.1, c_hi=35.4, c=x)
    elif x <= 55.4:
        return get_subindex(I_low=101, I_hi=150, c_low=35.5, c_hi=55.4, c=x)
    elif x <= 150.4:
        return get_subindex(I_low=151, I_hi=200, c_low=55.5, c_hi=150.4, c=x)
    elif x <= 250.4:
        return get_subindex(I_low=201, I_hi=300, c_low=150.5, c_hi=250.4, c=x)
    elif x <= 350.4:
        return get_subindex(I_low=301, I_hi=400, c_low=250.5, c_hi=350.4, c=x)
    elif x <= 500.4:
        return get_subindex(I_low=401, I_hi=500, c_low=350.5, c_hi=500.4, c=x)
    elif x > 500.4:
        return np.Inf
    else:
        return None


FUNCTION_MAP = {
    "CO": get_CO_subindex,
    "O3": get_O3_subindex,
    "NO2": get_NO2_subindex,
    "SO2": get_SO2_subindex,
    "PM10": get_PM10_subindex,
    "PM2.5": getPM25_subindex,
}


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def create_common_dataset(input_path: str, output_path: str):
    """
    Merge dataset with subindex and calculation AQI
    :param input_path: path with input data
    :param output_path: path to save file
    """
    with open(METADATA_POLLUTANT_PATH) as file:
        metadata = yaml.safe_load(file)

    with open(CONFIG_PATH) as json_file:
        config = json.load(json_file)

    dataset_merge = pd.DataFrame({})

    for pollutant in config["pollutants"]:
        path = f"{input_path}{config['country']}_{pollutant}_cleaned.csv"
        dataset = pd.read_csv(path)

        assert len(dataset["UnitOfMeasurement"].unique()) == 1
        if (
            metadata["units"][pollutant]
            != dataset["UnitOfMeasurement"].unique()[0]
        ):
            change_units(
                dataset, metadata["molar_mass"], metadata["units"][pollutant]
            )
        else:
            dataset["Concentration_correct"] = dataset["Concentration"]

        if metadata["average"][pollutant]["window"] > 1:
            dataset[f"{pollutant}_avg"] = (
                dataset["Concentration_correct"]
                .rolling(
                    window=metadata["average"][pollutant]["window"],
                    min_periods=metadata["average"][pollutant]["period"],
                )
                .mean()
                .values
            )
        else:
            dataset[f"{pollutant}_avg"] = dataset["Concentration_correct"]

        dataset[f"{pollutant}_SubIndex"] = round(
            dataset[f"{pollutant}_avg"].apply(
                lambda x: FUNCTION_MAP[pollutant](x)
            )
        )

        if dataset_merge.empty:
            dataset_merge = dataset[
                [
                    "Countrycode",
                    "AirQualityStationEoICode",
                    "Datetime",
                    f"{pollutant}_avg",
                    f"{pollutant}_SubIndex",
                ]
            ].copy()
        else:
            dataset_merge = pd.merge(
                dataset_merge,
                dataset[
                    [
                        "Countrycode",
                        "AirQualityStationEoICode",
                        "Datetime",
                        f"{pollutant}_avg",
                        f"{pollutant}_SubIndex",
                    ]
                ],
                how="left",
                on=["Countrycode", "AirQualityStationEoICode", "Datetime"],
            )

    dataset_merge["AQI"] = dataset_merge[
        [f"{p}_SubIndex" for p in config["pollutants"]]
    ].max(axis=1, skipna=False)
    dataset_merge.to_csv(output_path, index=False)


if __name__ == "__main__":
    create_common_dataset()
