import pandas as pd

df = pd.read_csv(
    "outputs/final/master_dataset.csv",
    low_memory=False
)

# Convert to string
df["Date"] = df["Date"].astype(str)

# Manual mappings
date_mapping = {

    "Sept": "2022-09",

    "Oct20": "2020-10",
    "Nov20": "2020-11",

    "May'24": "2024-05",
    "Jun'24": "2024-06",
    "Jul'24": "2024-07",
    "Aug'24": "2024-08",
    "Sep'24": "2024-09",
    "Oct'24": "2024-10",
    "Nov'24": "2024-11",
    "Dec'24": "2024-12",

    "Jan'25": "2025-01",
    'Jan"25': "2025-01",
    "Feb'25": "2025-02",
    "Mar'25": "2025-03",
    "Apr'25": "2025-04",
    "May'25": "2025-05",
    "Jun'25": "2025-06",
    "June'25": "2025-06",
    "Jul'25": "2025-07",
    "Aug'25": "2025-08",
    "Sep'25": "2025-09",
    "Oct'25": "2025-10",
    "Nov'25": "2025-11",
    "Dec'25": "2025-12",

    "Jan'26": "2026-01",
    "Feb'26": "2026-02",
    "Mar'26": "2026-03",
    "Apr'26": "2026-04"
}

# Apply mappings
df["Date"] = df["Date"].replace(date_mapping)

# Convert standard datetime strings
mask = df["Date"].str.contains("00:00:00", na=False)

df.loc[mask, "Date"] = pd.to_datetime(
    df.loc[mask, "Date"]
).dt.strftime("%Y-%m")

# Save cleaned dataset
df.to_csv(
    "outputs/final/master_dataset_standardized.csv",
    index=False
)

print("\nStandardized Dataset Created")

print("\nRows:", len(df))

print("\nUnique Dates:")
print(sorted(df["Date"].unique()))

print("\nTotal Unique Months:")
print(df["Date"].nunique())