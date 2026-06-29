import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

# Load data
df = pd.read_csv(
    "outputs/final/master_dataset_standardized.csv",
    low_memory=False
)

# Select part
part_number = "IM300205"

part_df = df[
    df["Part_No"].astype(str) == part_number
].copy()

# Aggregate across warehouses
part_df = (
    part_df.groupby("Date")["Demand"]
    .sum()
    .reset_index()
)

part_df = part_df.sort_values("Date")

# Train/Test Split
train = part_df.iloc[:-3]

test = part_df.iloc[-3:]

# ARIMA Model
model = ARIMA(
    train["Demand"],
    order=(1,1,1)
)

fit = model.fit()

forecast = fit.forecast(3)

# Metrics
mae = mean_absolute_error(
    test["Demand"],
    forecast
)

rmse = np.sqrt(
    mean_squared_error(
        test["Demand"],
        forecast
    )
)

mape = (
    np.mean(
        np.abs(
            (
                test["Demand"] - forecast
            ) / test["Demand"]
        )
    )
    * 100
)

accuracy = 100 - mape

print("\nActual Values")
print(test["Demand"].values)

print("\nForecast Values")
print(forecast.values)

print("\nMAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE:", round(mape, 2))
print("Accuracy:", round(accuracy, 2), "%")