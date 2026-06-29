import pandas as pd

# Load ABC-XYZ analysis
df = pd.read_csv(
    "outputs/abc_xyz_analysis.csv"
)

# Create combined category
df["ABC_XYZ"] = (
    df["ABC_Class"] +
    df["XYZ_Class"]
)

# Strategy Assignment
def assign_strategy(category):

    strategy_map = {

        "AX": "Holt-Winters",
        "AY": "ARIMA",
        "AZ": "ARIMA",

        "BX": "Holt",
        "BY": "ARIMA",
        "BZ": "ARIMA",

        "CX": "Moving Average",
        "CY": "Croston",
        "CZ": "Croston"
    }

    return strategy_map.get(
        category,
        "Moving Average"
    )

df["Forecast_Strategy"] = (
    df["ABC_XYZ"]
    .apply(assign_strategy)
)

# Save output
df.to_csv(
    "outputs/forecasting_strategy.csv",
    index=False
)

print("\nForecasting Strategy Distribution")
print(
    df["Forecast_Strategy"]
    .value_counts()
)

print("\nSample Records")
print(
    df[[
        "Part_No",
        "ABC_Class",
        "XYZ_Class",
        "Forecast_Strategy"
    ]].head(10)
)

print("\nForecasting Strategy File Created")