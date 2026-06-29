import pandas as pd

df = pd.read_csv("outputs/abc_analysis.csv")

def classify_xyz(cv):

    if cv <= 0.5:
        return "X"

    elif cv <= 1.0:
        return "Y"

    else:
        return "Z"

df["XYZ_Class"] = df["CV"].apply(classify_xyz)

df.to_csv(
    "outputs/abc_xyz_analysis.csv",
    index=False
)

print("\nXYZ Distribution")
print(
    df["XYZ_Class"]
    .value_counts()
)

print("\nABC-XYZ Matrix")
print(
    pd.crosstab(
        df["ABC_Class"],
        df["XYZ_Class"]
    )
)

print("\nXYZ Analysis Completed")