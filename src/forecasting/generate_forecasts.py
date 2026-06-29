import pandas as pd

from models.moving_average import moving_average_forecast
from models.simple_exponential import ses_forecast
from models.holt_linear import holt_forecast
from models.holt_winters import holt_winters_forecast
from models.arima import arima_forecast
from models.croston import croston_forecast

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

master_df = pd.read_csv(
    "outputs/final/top_a_parts.csv"
)

best_models = pd.read_csv(
    "outputs/final/best_model_by_part.csv"
)

# ---------------------------------------------------
# FORECAST HORIZONS
# ---------------------------------------------------

FORECAST_HORIZONS = [1, 3, 6, 12]

# ---------------------------------------------------
# GENERATE FORECASTS
# ---------------------------------------------------

for FORECAST_HORIZON in FORECAST_HORIZONS:

    print(f"\nGenerating {FORECAST_HORIZON}-Month Forecast...")

    results = []

    for _, row in best_models.iterrows():

        part = row["Part_No"]
        model_name = row["Best_Model"]

        part_df = (
            master_df[
                master_df["Part_No"] == part
            ]
            .sort_values("Date")
        )

        series = part_df["Demand"]

        if model_name == "Moving Average":

            result = moving_average_forecast(
                series,
                forecast_periods=FORECAST_HORIZON
            )

        elif model_name == "Simple Exponential Smoothing":

            result = ses_forecast(
                series,
                forecast_periods=FORECAST_HORIZON
            )

        elif model_name == "Holt Linear":

            result = holt_forecast(
                series,
                forecast_periods=FORECAST_HORIZON
            )

        elif model_name == "Holt-Winters":

            result = holt_winters_forecast(
                series,
                forecast_periods=FORECAST_HORIZON
            )

        elif model_name == "ARIMA":

            result = arima_forecast(
                series,
                forecast_periods=FORECAST_HORIZON
            )

        elif model_name == "Croston":

            result = croston_forecast(
                series,
                forecast_periods=FORECAST_HORIZON
            )

        else:
            continue

        if result is None:
            continue

        for month, value in enumerate(
            result["Forecast"],
            start=1
        ):

            results.append({

                "Part_No": part,

                "Best_Model": model_name,

                "Forecast_Month": month,

                "Forecast_Value": round(
                    float(value),
                    2
                )

            })

    forecast_df = pd.DataFrame(results)

    forecast_df.to_csv(
        f"outputs/final/forecast_results_{FORECAST_HORIZON}.csv",
        index=False
    )

    print(
        f"{FORECAST_HORIZON}-Month Forecast Saved"
    )

    print(
        forecast_df.head()
    )

    print(
        f"Total Forecast Records: {len(forecast_df)}"
    )

print("\nAll Forecast Horizons Generated Successfully.")