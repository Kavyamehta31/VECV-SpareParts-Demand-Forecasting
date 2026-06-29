import pandas as pd

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

inventory_df = pd.read_csv(
    "outputs/final/inventory_optimization.csv"
)

abc_xyz_df = pd.read_csv(
    "outputs/abc_xyz_analysis.csv"
)

# ---------------------------------------
# DEBUG INFORMATION
# ---------------------------------------

print("Inventory Shape:", inventory_df.shape)
print("ABC XYZ Shape:", abc_xyz_df.shape)

print(
    "ABC XYZ Duplicate Warehouse+Part:",
    abc_xyz_df.duplicated(
        subset=["Warehouse", "Part_No"]
    ).sum()
)

# ---------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------

abc_xyz_df = abc_xyz_df.drop_duplicates(
    subset=["Warehouse", "Part_No"],
    keep="first"
)

print("ABC XYZ Shape After Cleanup:", abc_xyz_df.shape)

# ---------------------------------------
# MERGE
# ---------------------------------------

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

print("Merged Shape:", df.shape)

# ---------------------------------------
# RECOMMENDATION LOGIC
# ---------------------------------------

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

# ---------------------------------------
# APPLY RECOMMENDATIONS
# ---------------------------------------

df["Recommendation"] = df.apply(
    generate_recommendation,
    axis=1
)

# ---------------------------------------
# SAVE
# ---------------------------------------

df.to_csv(
    "outputs/final/recommendations.csv",
    index=False
)

print("\nRecommendation Engine Completed")
print("Final Shape:", df.shape)

print("\nTop Recommendations")
print(df["Recommendation"].value_counts())