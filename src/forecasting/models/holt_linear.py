import pandas as pd
from statsmodels.tsa.holtwinters import Holt


def holt_forecast(
    series,
    forecast_periods=3
):

    try:

        series = pd.Series(series).dropna().astype(float)

        if len(series) < 5:
            return None

        model = Holt(
            series
        ).fit()

        forecast = model.forecast(
            forecast_periods
        )

        return {
            "Model": "Holt Linear",
            "Forecast": forecast.tolist()
        }

    except:
        return None