import os

import pytest
import pandas as pd
import great_expectations as ge


EXTERNAL_PATH = "data/external/"


def test_output():
    files = os.listdir(EXTERNAL_PATH)
    files.remove(".gitignore")
    if len(files) != 0:
        for file in files:
            df = pd.read_csv(f"{EXTERNAL_PATH}{file}", index_col=False, encoding="latin1")
            df_ge = ge.from_pandas(df)
            expected_columns = [
                "network_countrycode",
                "network_localid",
                "network_name",
                "network_namespace",
                "network_timezone",
                "pollutant",
                "samplingpoint_localid",
                "samplingpoint_namespace",
                "samplingpoint_x",
                "samplingpoint_y",
                "coordsys",
                "station_code",
                "station_localid",
                "station_name",
                "station_namespace",
                "value_datetime_begin",
                "value_datetime_end",
                "value_datetime_inserted",
                "value_datetime_updated",
                "value_numeric",
                "value_validity",
                "value_verification",
                "station_altitude",
                "value_unit",
            ]
            assert (
                df_ge.expect_table_columns_to_match_ordered_list(
                    column_list=expected_columns
                ).success
                is True
            )
            assert (
                df_ge.expect_column_values_to_not_be_null(column="value_datetime_begin").success
                is True
            )
            assert (
                df_ge.expect_column_values_to_not_be_null(column="value_datetime_end").success is True
            )
            assert (
                    df_ge.expect_column_values_to_not_be_null(
                        column="station_code").success is True
            )
            assert (
                df_ge.expect_column_values_to_be_of_type(
                    column="value_numeric", type_="float64"
                ).success
                is True
            )

