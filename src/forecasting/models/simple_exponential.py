import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


def ses_forecast(
    series,
    forecast_periods=3
):

    try:

        series = pd.Series(series).dropna().astype(float)

        if len(series) < 5:
            return None

        model = SimpleExpSmoothing(
            series
        ).fit()

        forecast = model.forecast(
            forecast_periods
        )

        return {
            "Model": "Simple Exponential Smoothing",
            "Forecast": forecast.tolist()
        }

    except:
        return None