from typing import List, Dict, Tuple, Any
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


def create_x_y_datasets(
    df: pd.DataFrame, cols: List[str], depth: int
) -> Tuple[pd.DataFrame, pd.Series]:
    """

    :param df: dataframe
    :param cols: list of column names
    :param depth: number of shift
    :return: tables
    """
    y = df["AQI"].copy()
    x_list = [df[cols].shift(i) for i in range(1, depth + 1)]
    x = pd.concat(x_list, axis=1)
    x.columns = list(range(len(x.columns)))

    x = x.iloc[depth:]
    y = y.iloc[depth:]
    return x, y


def choose_day_number(
    columns: List[str], df: pd.DataFrame, n: int, model
) -> Dict[str, List[float]]:
    """
    Default
    :param columns: list of column names
    :param df: dataset
    :param n: number of shift
    :param model_tag: model tag for fitting
    :return: dict with rmse and mae
    """
    rmse_dict = {"rmse": [], "mae": []}
    for depth in range(1, n):
        x, y = create_x_y_datasets(df, columns, depth)

        X_train, X_test, y_train, y_test = train_test_split(
            x, y, shuffle=False, random_state=42
        )

        model.fit(X_train, y_train)

        y_hat = model.predict(X_test)

        rmse_dict["rmse"].append(mean_squared_error(y_test, y_hat, squared=False))
        rmse_dict["mae"].append(mean_absolute_error(y_test, y_hat))

    return rmse_dict


def search_best_params(
    columns: List[str], df: pd.DataFrame, depth: int, n_cv: int, grid: Dict, model
):
    """
    Random search hyperparameters
    :param columns: list of column names
    :param df: dataset
    :param depth: number of shift
    :param model: model for fitting
    :param n_cv: cross-validation split number
    :param grid: grid of parameters
    :return: model with best parameters
    """
    x, y = create_x_y_datasets(df, columns, depth)

    tscv = TimeSeriesSplit(n_splits=n_cv)
    rf_random = RandomizedSearchCV(
        estimator=model,
        param_distributions=grid,
        n_iter=500,
        cv=tscv,
        verbose=0,
        random_state=42,
        n_jobs=-1,
    )

    rf_random.fit(x, y)
    return rf_random.best_estimator_


def predict_best_model(
    df: pd.DataFrame, columns: List[str], depth: int, model
) -> Tuple[float, float]:
    """
    Error of best model prediction
    :param columns: list of column names
    :param df: dataset
    :param depth: number of shift
    :param model: model for fitting
    :return: error tuple
    """
    x, y = create_x_y_datasets(df, columns, depth)
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, shuffle=False, random_state=42
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    best_rmse = mean_squared_error(y_test, predictions, squared=False)
    best_mae = mean_absolute_error(y_test, predictions)

    return best_rmse, best_mae
