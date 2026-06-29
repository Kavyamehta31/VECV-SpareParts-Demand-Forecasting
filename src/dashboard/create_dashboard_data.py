import pandas as pd

# Demand Profile
profile_df = pd.read_csv(
    "outputs/demand_profile.csv"
)

# Inventory
inventory_df = pd.read_csv(
    "outputs/final/inventory_optimization.csv"
)

# ABC XYZ
abc_xyz_df = pd.read_csv(
    "outputs/abc_xyz_analysis.csv"
)

# Warehouse Summary
warehouse_summary = (
    profile_df.groupby("Warehouse")
    .agg({
        "Total_Demand": "sum",
        "Part_No": "count"
    })
    .reset_index()
)

warehouse_summary.to_csv(
    "app/data/warehouse_summary.csv",
    index=False
)

# ABC Summary
abc_summary = (
    abc_xyz_df["ABC_Class"]
    .value_counts()
    .reset_index()
)

abc_summary.columns = [
    "ABC_Class",
    "Count"
]

abc_summary.to_csv(
    "app/data/abc_summary.csv",
    index=False
)

# XYZ Summary
xyz_summary = (
    abc_xyz_df["XYZ_Class"]
    .value_counts()
    .reset_index()
)

xyz_summary.columns = [
    "XYZ_Class",
    "Count"
]

xyz_summary.to_csv(
    "app/data/xyz_summary.csv",
    index=False
)

# Risk Summary
risk_summary = (
    inventory_df["Inventory_Risk"]
    .value_counts()
    .reset_index()
)

risk_summary.columns = [
    "Inventory_Risk",
    "Count"
]

risk_summary.to_csv(
    "app/data/risk_summary.csv",
    index=False
)

print("Dashboard Data Created Successfully")