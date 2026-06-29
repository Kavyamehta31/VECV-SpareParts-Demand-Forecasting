import pandas as pd

from evaluate_models import evaluate_models

# -----------------------------------------
# Load Dataset
# -----------------------------------------

df = pd.read_csv(
    "outputs/final/top_a_parts.csv"
)

results = []

# -----------------------------------------
# Evaluate Every Part
# -----------------------------------------

for part in sorted(df["Part_No"].unique()):

    part_df = (

        df[df["Part_No"] == part]

        .sort_values("Date")

    )

    series = part_df["Demand"]

    evaluation = evaluate_models(series)

    if evaluation is None:
        continue

    best = evaluation.loc[
        evaluation["Accuracy"].idxmax()
    ]

    results.append({

        "Part_No": part,

        "Best_Model": best["Model"],

        "Accuracy": best["Accuracy"],

        "MAE": best["MAE"],

        "RMSE": best["RMSE"],

        "MAPE": best["MAPE"],

        "Bias": best["Bias"]

    })

# -----------------------------------------
# Save Results
# -----------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "outputs/final/best_model_by_part.csv",
    index=False
)

print(results_df.head())

print("\nTotal Parts Evaluated:", len(results_df))