from statsmodels.tsa.arima.model import ARIMA


def arima_forecast(series, forecast_periods=3):

    try:
        model = ARIMA(
            series,
            order=(1, 1, 1)
        )

        fit = model.fit()

        forecast = fit.forecast(forecast_periods)

        return {
            "Model": "ARIMA",
            "Forecast": forecast.tolist()
        }

    except:
        return None