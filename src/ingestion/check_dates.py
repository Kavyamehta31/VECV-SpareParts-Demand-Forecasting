import pandas as pd

df = pd.read_csv(
    "outputs/final/master_dataset.csv",
    low_memory=False
)

print(df["Date"].unique()[:100])