import pandas as pd

forecast_data = {
    "Month": [
        "2025-11",
        "2025-12",
        "2026-01",
        "2026-02",
        "2026-03",
        "2026-04"
    ],
    "Actual": [
        26060,
        31100,
        22160,
        None,
        None,
        None
    ],
    "Forecast": [
        None,
        None,
        None,
        34567,
        32157,
        30846
    ]
}

df = pd.DataFrame(forecast_data)

df.to_csv(
    "app/data/forecast_results.csv",
    index=False
)

print("Forecast Dashboard Data Created")