from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd


def holt_winters_forecast(
    series,
    forecast_periods=3
):

    try:

        series = pd.Series(series).dropna().astype(float)

        if len(series) < 5:
            return None

        model = ExponentialSmoothing(
            series,
            trend="add",
            seasonal=None
        )

        fit = model.fit()

        forecast = fit.forecast(
            forecast_periods
        )

        return {
            "Model": "Holt-Winters",
            "Forecast": forecast.tolist()
        }

    except:
        return None