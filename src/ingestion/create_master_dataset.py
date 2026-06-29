import pandas as pd

excel_file = "data/raw/file1.xlsx"

xls = pd.ExcelFile(excel_file)

master_data = []

for sheet in xls.sheet_names:

    print(f"Processing Warehouse {sheet}...")

    df = pd.read_excel(
        excel_file,
        sheet_name=sheet
    )

    # Fill missing values
    df = df.fillna(0)

    # Add warehouse column
    df["Warehouse"] = sheet

    # Identify non-demand columns
    id_columns = [
        "Warehouse",
        "Part No"
    ]

    if "Material Description" in df.columns:
        id_columns.append(
            "Material Description"
        )

    # Demand columns
    demand_columns = []

    for col in df.columns:

        if col not in id_columns and col != "Total_Demand":

            demand_columns.append(col)

    # Convert Wide → Long
    long_df = pd.melt(
        df,
        id_vars=id_columns,
        value_vars=demand_columns,
        var_name="Date",
        value_name="Demand"
    )

    master_data.append(long_df)

# Combine all warehouses
master_df = pd.concat(
    master_data,
    ignore_index=True
)

# Rename columns
master_df.rename(
    columns={
        "Part No": "Part_No",
        "Material Description":
        "Material_Description"
    },
    inplace=True
)

# Save output
master_df.to_csv(
    "outputs/final/master_dataset.csv",
    index=False
)

print("\nMaster Dataset Created")

print(
    "\nRows:",
    len(master_df)
)

print(
    "\nColumns:",
    len(master_df.columns)
)

print("\nSample Data:")

print(master_df.head())