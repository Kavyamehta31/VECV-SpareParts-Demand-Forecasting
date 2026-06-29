import pandas as pd

df = pd.read_csv(
    "outputs/final/master_dataset.csv",
    low_memory=False
)

# Convert date column to string
df["Date"] = df["Date"].astype(str)

# Keep only records that can be converted
df["Parsed_Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# Remove invalid dates
df = df[
    df["Parsed_Date"].notna()
]

# Standardize format
df["Date"] = (
    df["Parsed_Date"]
    .dt.strftime("%Y-%m")
)

# Remove helper column
df.drop(
    columns=["Parsed_Date"],
    inplace=True
)

df.to_csv(
    "outputs/final/master_dataset_clean.csv",
    index=False
)

print("\nClean Dataset Created")

print(
    "\nRows:",
    len(df)
)

print(
    "\nDate Range:"
)

print(df["Date"].min())

print(df["Date"].max())