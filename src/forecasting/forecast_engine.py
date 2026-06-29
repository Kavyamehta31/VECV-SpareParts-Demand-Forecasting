import pandas as pd

from evaluate_models import evaluate_models


def forecast_engine(series):
    """
    Runs all forecasting models,
    evaluates them,
    and returns the best model.
    """

    evaluation = evaluate_models(series)

    if evaluation is None:
        return None

    best = evaluation.loc[
        evaluation["Accuracy"].idxmax()
    ]

    return {
        "Best_Model": best["Model"],
        "Accuracy": best["Accuracy"],
        "MAE": best["MAE"],
        "RMSE": best["RMSE"],
        "MAPE": best["MAPE"],
        "Evaluation": evaluation
    }