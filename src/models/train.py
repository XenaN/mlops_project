import os
import click
import joblib as jb
from typing import List

import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()
remote_server_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(remote_server_uri)


@click.command()
@click.argument("input_path", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def train(input_path: List[str], output_path: str):
    """

    :param input_path:
    :param output_path:
    :return:
    """
    with mlflow.start_run():
        train_df = pd.read_csv(input_path[0])
        test_df = pd.read_csv(input_path[1])
        assert isinstance(train_df, pd.DataFrame)
        assert isinstance(test_df, pd.DataFrame)

        train_X = train_df["AQI"].values.reshape(-1, 1)
        train_y = train_df["AQI_t+1"].values

        test_X = test_df["AQI"].values.reshape(-1, 1)
        test_y = test_df["AQI_t+1"].values

        params = {
            "n_estimators": 800,
            "min_samples_split": 3,
            "min_samples_leaf": 5,
            "max_depth": 65,
            "bootstrap": True,
        }

        mlflow.log_params(params)

        forest_model = RandomForestRegressor(random_state=42, **params)
        forest_model.fit(train_X, train_y)
        jb.dump(forest_model, output_path)

        y_predicted = forest_model.predict(test_X)

        score = dict(rmse=mean_squared_error(test_y, y_predicted, squared=False),
                     mae=mean_absolute_error(test_y, y_predicted))

        mlflow.log_metrics(score)
        mlflow.sklearn.log_model(
            sk_model=forest_model,
            artifact_path="model",
            registered_model_name="forest_model",
        )


if __name__ == "__main__":
    train()
