import os
import click
import joblib as jb
from typing import List

import mlflow
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor
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
    Find the best hyperparameters, train model and tracking experiment by mlflow
    :param input_path: path of train and test datasets
    :param output_path: path for saving model
    """
    with mlflow.start_run():
        train_df = pd.read_csv(input_path[0])
        test_df = pd.read_csv(input_path[1])
        assert isinstance(train_df, pd.DataFrame)
        assert isinstance(test_df, pd.DataFrame)

        train_y = train_df["AQI"]
        train_X = train_df.drop("AQI", axis=1)

        test_y = test_df["AQI"]
        test_X = test_df.drop("AQI", axis=1)

        tscv = TimeSeriesSplit(n_splits=3)

        model = XGBRegressor(random_state=0, verbosity=0)

        grid = {
            "n_estimators": [100, 500, 1000],
            "min_child_weight": [4, 5],
            "gamma": [i / 10.0 for i in range(3, 6)],
            "subsample": [i / 10.0 for i in range(6, 11)],
            "colsample_bytree": [i / 10.0 for i in range(6, 11)],
            "max_depth": [2, 3, 4, 6, 7, 10, 15],
            "objective": ["reg:squarederror", "reg:tweedie"],
            "booster": ["gbtree", "gblinear"],
            "eval_metric": ["rmse"],
            "eta": [i / 10.0 for i in range(3, 6)],
            "learning_rate": [0.01, 0.1, 0.2, 0.3],
        }
        rf_random = RandomizedSearchCV(
            estimator=model,
            param_distributions=grid,
            n_iter=500,
            cv=tscv,
            verbose=0,
            random_state=42,
            n_jobs=-1,
        )

        rf_random.fit(train_X, train_y)
        params = rf_random.best_params_

        mlflow.log_params(params)

        best_model = XGBRegressor(random_state=0, **params)
        best_model.fit(train_X, train_y)
        jb.dump(best_model, output_path)

        y_predicted = best_model.predict(test_X)

        score = dict(
            rmse=mean_squared_error(test_y, y_predicted, squared=False),
            mae=mean_absolute_error(test_y, y_predicted),
        )

        mlflow.log_metrics(score)
        mlflow.sklearn.log_model(
            sk_model=best_model,
            artifact_path="model",
            registered_model_name="xgb_model",
        )


if __name__ == "__main__":
    train()
