import pandas as pd
import numpy as np

# Excel file path
excel_file = "data/raw/file1.xlsx"

# Load workbook
xls = pd.ExcelFile(excel_file)

# Store all profiles
all_profiles = []

# Process each warehouse sheet
for sheet in xls.sheet_names:

    print(f"Processing Warehouse {sheet}...")

    # Read sheet
    df = pd.read_excel(
        excel_file,
        sheet_name=sheet
    )

    # Replace missing values with 0
    df = df.fillna(0)

    # Identify demand columns
    demand_columns = []

    for col in df.columns:
        if col not in [
            "Part No",
            "Material Description",
            "Total_Demand"
        ]:
            demand_columns.append(col)

    # Process each spare part
    for _, row in df.iterrows():

        demand = row[demand_columns].values

        # Basic metrics
        total_demand = np.sum(demand)
        avg_demand = np.mean(demand)
        std_demand = np.std(demand)

        # Number of months with demand
        non_zero_months = np.count_nonzero(demand)

        # Coefficient of Variation
        if avg_demand == 0:
            cv = 0
        else:
            cv = std_demand / avg_demand

        # Intermittency Rate
        intermittency_rate = (
            len(demand_columns) - non_zero_months
        ) / len(demand_columns)

        # Demand Classification
        if total_demand == 0:
            demand_class = "Dead Stock"

        elif non_zero_months < 6:
            demand_class = "Intermittent"

        elif non_zero_months < 24:
            demand_class = "Slow Moving"

        else:
            demand_class = "Fast Moving"

        # Store profile
        profile = {
            "Warehouse": sheet,
            "Part_No": row["Part No"],
            "Total_Demand": round(total_demand, 2),
            "Avg_Demand": round(avg_demand, 2),
            "Std_Demand": round(std_demand, 2),
            "CV": round(cv, 2),
            "Non_Zero_Months": non_zero_months,
            "Intermittency_Rate": round(intermittency_rate, 2),
            "Demand_Class": demand_class
        }

        all_profiles.append(profile)

# Create DataFrame
profile_df = pd.DataFrame(all_profiles)

# Save output file
profile_df.to_csv(
    "outputs/demand_profile.csv",
    index=False
)

# Display sample output
print("\nDemand Profile Sample:")
print(profile_df.head())

print("\nTotal Parts Profiled:", len(profile_df))

print("\nDemand Profile Created Successfully")
print("Saved to outputs/demand_profile.csv")