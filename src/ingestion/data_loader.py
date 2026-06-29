import pandas as pd

excel_file = "data/raw/file1.xlsx"

xls = pd.ExcelFile(excel_file)

for sheet in xls.sheet_names:

    df = pd.read_excel(
        excel_file,
        sheet_name=sheet
    )

    print("\n" + "="*70)
    print(f"SHEET: {sheet}")
    print("="*70)

    print(df.head())