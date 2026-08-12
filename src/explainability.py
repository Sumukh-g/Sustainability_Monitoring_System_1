"""Model association summaries; importance does not establish causality."""

import numpy as np
import pandas as pd


def feature_importance(artifact: dict) -> pd.DataFrame:
    model = artifact["model"]
    values = getattr(model, "feature_importances_", None)
    if values is None:
        values = np.abs(getattr(model, "coef_", np.zeros(len(artifact["features"]))))
    return pd.DataFrame(
        {"feature": artifact["features"], "importance": values}
    ).sort_values("importance", ascending=False)
