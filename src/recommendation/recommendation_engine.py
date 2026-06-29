import pandas as pd

# Load datasets
inventory_df = pd.read_csv(
    "outputs/final/inventory_optimization.csv"
)

abc_xyz_df = pd.read_csv(
    "outputs/abc_xyz_analysis.csv"
)

# Merge
df = inventory_df.merge(
    abc_xyz_df[
        [
            "Warehouse",
            "Part_No",
            "ABC_Class",
            "XYZ_Class"
        ]
    ],
    on=[
        "Warehouse",
        "Part_No"
    ],
    how="left"
)

# Recommendation Logic
def generate_recommendation(row):

    if row["Demand_Class"] == "Dead Stock":
        return "Review for disposal or inventory reduction"

    if (
        row["ABC_Class"] == "A"
        and row["XYZ_Class"] == "Z"
    ):
        return "Maintain higher safety stock and monitor closely"

    if (
        row["ABC_Class"] == "A"
        and row["XYZ_Class"] == "X"
    ):
        return "Prioritize replenishment and forecasting"

    if row["Inventory_Risk"] == "High Risk":
        return "Increase monitoring and review reorder point"

    if row["Demand_Class"] == "Intermittent":
        return "Use Croston forecasting method"

    if row["Demand_Class"] == "Fast Moving":
        return "Maintain adequate stock levels"

    return "Regular inventory review"

# Apply
df["Recommendation"] = (
    df.apply(
        generate_recommendation,
        axis=1
    )
)

# Save
df.to_csv(
    "outputs/final/recommendations.csv",
    index=False
)

print("\nRecommendation Engine Completed")

print("\nTop Recommendations")

print(
    df["Recommendation"]
    .value_counts()
)

print("\nSample Output")

print(
    df[
        [
            "Part_No",
            "ABC_Class",
            "XYZ_Class",
            "Inventory_Risk",
            "Recommendation"
        ]
    ]
    .head(10)
)