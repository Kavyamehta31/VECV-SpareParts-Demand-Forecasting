import pandas as pd

# Load demand profile
df = pd.read_csv("outputs/demand_profile.csv")

# Sort by total demand
df = df.sort_values(
    by="Total_Demand",
    ascending=False
)

# Calculate demand contribution
total_demand = df["Total_Demand"].sum()

df["Demand_Percentage"] = (
    df["Total_Demand"] / total_demand
) * 100

# Calculate cumulative percentage
df["Cumulative_Percentage"] = (
    df["Demand_Percentage"]
    .cumsum()
)

# Assign ABC Category
def classify_abc(value):

    if value <= 80:
        return "A"

    elif value <= 95:
        return "B"

    else:
        return "C"

df["ABC_Class"] = (
    df["Cumulative_Percentage"]
    .apply(classify_abc)
)

# Save output
df.to_csv(
    "outputs/abc_analysis.csv",
    index=False
)

print("\nABC Distribution")
print(
    df["ABC_Class"]
    .value_counts()
)

print("\nTop 10 A-Class Parts")
print(
    df[
        df["ABC_Class"] == "A"
    ][[
        "Warehouse",
        "Part_No",
        "Total_Demand"
    ]]
    .head(10)
)

print("\nABC Analysis Completed")