import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from models.moving_average import moving_average_forecast
from models.simple_exponential import ses_forecast
from models.holt_linear import holt_forecast
from models.holt_winters import holt_winters_forecast
from models.arima import arima_forecast
from models.croston import croston_forecast


# --------------------------------------------
# Evaluation Function
# --------------------------------------------

def evaluate_models(series):

    series = pd.Series(series).dropna().astype(float)

    if len(series) < 12:
        return None

    train = series.iloc[:-3]

    test = series.iloc[-3:]

    models = [

        moving_average_forecast(
            train,
            forecast_periods=3
        ),

        ses_forecast(
            train,
            forecast_periods=3
        ),

        holt_forecast(
            train,
            forecast_periods=3
        ),

        holt_winters_forecast(
            train,
            forecast_periods=3
        ),

        arima_forecast(
            train,
            forecast_periods=3
        ),

        croston_forecast(
            train,
            forecast_periods=3
        )

    ]

    results = []

    for model in models:

        if model is None:
            continue

        forecast = np.array(model["Forecast"])

        actual = np.array(test)

        mae = mean_absolute_error(
            actual,
            forecast
        )

        rmse = np.sqrt(
            mean_squared_error(
                actual,
                forecast
            )
        )
        bias = np.mean(
            forecast - actual
        )

        mape = np.mean(

            np.abs(

                (actual - forecast)

                /

                np.where(actual == 0, 1, actual)

            )

        ) * 100

        accuracy = max(0, 100 - mape)

        results.append({

            "Model": model["Model"],

            "MAE": round(mae, 2),

            "RMSE": round(rmse, 2),

            "MAPE": round(mape, 2),

            "Bias": round(bias, 2),

            "Accuracy": round(accuracy, 2)

        })

    results_df = pd.DataFrame(results)

    return results_df