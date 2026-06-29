import pandas as pd

excel_file = "data/raw/file1.xlsx"

xls = pd.ExcelFile(excel_file)

for sheet in xls.sheet_names:

    df = pd.read_excel(
        excel_file,
        sheet_name=sheet
    )

    print("\n" + "="*70)
    print(f"WAREHOUSE : {sheet}")
    print("="*70)

    print(f"Total Parts : {len(df)}")

    missing_values = df.isnull().sum().sum()

    print(f"Missing Values : {missing_values}")

    duplicate_parts = df["Part No"].duplicated().sum()

    print(f"Duplicate Parts : {duplicate_parts}")