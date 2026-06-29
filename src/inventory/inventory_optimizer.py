import pandas as pd
import numpy as np

# Load demand profile
df = pd.read_csv(
    "outputs/demand_profile.csv"
)

# Assumptions
SERVICE_LEVEL_Z = 1.65
LEAD_TIME_MONTHS = 1

# Safety Stock
df["Safety_Stock"] = (
    SERVICE_LEVEL_Z *
    df["Std_Demand"]
)

# Reorder Point
df["Reorder_Point"] = (
    df["Avg_Demand"] *
    LEAD_TIME_MONTHS
) + df["Safety_Stock"]
# Target Stock Level
df["Target_Stock_Level"] = (
    df["Reorder_Point"] +
    df["Avg_Demand"] * LEAD_TIME_MONTHS
)
# Inventory Coverage (Months)
df["Inventory_Coverage"] = np.where(
    df["Avg_Demand"] > 0,
    df["Target_Stock_Level"] / df["Avg_Demand"],
    0
)
# Service Level Achievement (%)
df["Service_Level_Achievement"] = (
    SERVICE_LEVEL_Z / 1.65
) * 100
# Inventory Risk Classification
def classify_risk(row):

    if row["Demand_Class"] == "Dead Stock":
        return "Dead Inventory"

    elif row["CV"] > 2:
        return "High Risk"

    elif row["CV"] > 1:
        return "Medium Risk"

    else:
        return "Low Risk"

df["Inventory_Risk"] = (
    df.apply(
        classify_risk,
        axis=1
    )
)

# Save
df.to_csv(
    "outputs/final/inventory_optimization.csv",
    index=False
)

print("\nInventory Optimization Completed")

print("\nInventory Risk Distribution")
print(
    df["Inventory_Risk"]
    .value_counts()
)

print("\nSample Output")
print(
    df[[
        "Part_No",
        "Avg_Demand",
        "Std_Demand",
        "Safety_Stock",
        "Reorder_Point",
        "Target_Stock_Level",
        "Inventory_Coverage",
        "Service_Level_Achievement",
        "Inventory_Risk"
    ]]
    .head()
)