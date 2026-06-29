import pandas as pd

# Load demand profile
df = pd.read_csv("outputs/demand_profile.csv")

print("\n" + "="*60)
print("DEMAND CLASS DISTRIBUTION")
print("="*60)

print(df["Demand_Class"].value_counts())

print("\n" + "="*60)
print("WAREHOUSE WISE PART COUNT")
print("="*60)

print(df.groupby("Warehouse")["Part_No"].count())

print("\n" + "="*60)
print("WAREHOUSE WISE TOTAL DEMAND")
print("="*60)

print(
    df.groupby("Warehouse")["Total_Demand"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "="*60)
print("TOP 10 PARTS BY TOTAL DEMAND")
print("="*60)

print(
    df.sort_values(
        by="Total_Demand",
        ascending=False
    )[[
        "Warehouse",
        "Part_No",
        "Total_Demand"
    ]].head(10)
)