import pandas as pd
import numpy as np


def croston_forecast(
    series,
    alpha=0.1,
    forecast_periods=3
):

    try:

        series = pd.Series(series).fillna(0).astype(float)

        demand = series.values

        if np.count_nonzero(demand) == 0:
            return None

        z = []
        p = []

        interval = 1

        for value in demand:

            if value > 0:

                z.append(value)
                p.append(interval)
                interval = 1

            else:

                interval += 1

        z_hat = z[0]
        p_hat = p[0]

        for i in range(1, len(z)):

            z_hat = alpha * z[i] + (1 - alpha) * z_hat
            p_hat = alpha * p[i] + (1 - alpha) * p_hat

        forecast = z_hat / p_hat

        return {
            "Model": "Croston",
            "Forecast": [forecast] * forecast_periods
        }

    except:
        return None