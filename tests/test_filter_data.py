import json

import pytest
import pandas as pd
from src import filter_data
from click.testing import CliRunner
import great_expectations as ge


runner = CliRunner()
CONFIG_PATH = "metadata/download_config.json"
with open(CONFIG_PATH) as json_file:
    CONFIG = json.load(json_file)


def test_cli_command():
    result = runner.invoke(
        filter_data,
        f"data/raw/{CONFIG['country']}_CO/ "
        f"data/interim/filtered/{CONFIG['country']}_CO_filtered.csv",
    )
    assert result.exit_code == 0


def test_output():
    df = pd.read_csv(f"data/interim/filtered/{CONFIG['country']}_CO_filtered.csv")
    df_ge = ge.from_pandas(df)
    expected_columns = [
        "Countrycode",
        "Namespace",
        "AirQualityNetwork",
        "AirQualityStation",
        "AirQualityStationEoICode",
        "SamplingPoint",
        "SamplingProcess",
        "Sample",
        "AirPollutant",
        "AirPollutantCode",
        "AveragingTime",
        "Concentration",
        "UnitOfMeasurement",
        "DatetimeBegin",
        "DatetimeEnd",
        "Validity",
        "Verification",
    ]
    assert (
        df_ge.expect_table_columns_to_match_ordered_list(
            column_list=expected_columns
        ).success
        is True
    )
    assert (
        df_ge.expect_column_values_to_be_unique(column="DatetimeBegin").success is True
    )
    assert df_ge.expect_column_values_to_be_unique(column="DatetimeEnd").success is True
    assert (
        df_ge.expect_column_values_to_not_be_null(column="DatetimeBegin").success
        is True
    )
    assert (
        df_ge.expect_column_values_to_not_be_null(column="DatetimeEnd").success is True
    )
    assert (
        df_ge.expect_column_values_to_be_of_type(
            column="Concentration", type_="float64"
        ).success
        is True
    )
