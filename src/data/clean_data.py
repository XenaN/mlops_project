import click

import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def clean_data(input_path: str, output_path: str):
    """
    Some checks and fill datetime if there is missed data
    :param input_path: path with input data
    :param output_path: path to save file
    """
    table = pd.read_csv(
        input_path, parse_dates=["Datetime"], index_col=["Datetime"]
    )

    assert len(table["UnitOfMeasurement"].unique()) == 1
    if table["DatetimeEnd"].duplicated().any():
        index = table[table["DatetimeEnd"].duplicated(keep=False)].index
        index_validity = table.loc[index].query("Validity == -1").index
        table = table.drop(index_validity)
    assert not table["DatetimeEnd"].duplicated().any()

    if not table.query("Validity == -1")["Concentration"].isnull().all():
        table.query("Validity == -1")["Concentration"] = None

    if (
        len(pd.to_datetime(table["DatetimeEnd"]).diff().value_counts().values)
        != 1
    ):
        mask = table.index

        table = table.resample("H").ffill()
        diff = table.index.difference(mask)
        table.loc[diff, "Concentration"] = None

    table = table.reset_index(level=0)

    table.to_csv(output_path, index=False)


if __name__ == "__main__":
    clean_data()
