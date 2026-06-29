import pandas as pd


def moving_average_forecast(
    series,
    window=3,
    forecast_periods=3
):

    try:

        series = pd.Series(series).dropna().astype(float)

        if len(series) < window:
            return None

        history = series.tolist()

        forecasts = []

        for _ in range(forecast_periods):

            prediction = sum(
                history[-window:]
            ) / window

            forecasts.append(prediction)

            history.append(prediction)

        return {
            "Model": "Moving Average",
            "Forecast": forecasts
        }

    except:
        return None