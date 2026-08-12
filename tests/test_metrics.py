import numpy as np
import pandas as pd
from src.sustainability_metrics import (
    calculate_pue,
    calculate_wue,
    calculate_cue,
    sustainability_score,
)


def test_metric_formulas_and_invalid_denominators():
    d = pd.Series([100.0, 0.0, np.nan])
    assert calculate_pue(pd.Series([150.0, 10.0, 10.0]), d).iloc[0] == 1.5
    assert calculate_wue(pd.Series([200.0, 1.0, 1.0]), d).iloc[0] == 2
    assert calculate_cue(pd.Series([30.0, 1.0, 1.0]), d).iloc[0] == 0.3
    assert calculate_pue(pd.Series([1.0, 1.0, 1.0]), d).iloc[1:].isna().all()


def test_score_is_bounded(sample_data):
    score, label = sustainability_score(sample_data)
    assert 0 <= score <= 100
    assert label in {"Excellent", "Good", "Moderate", "Poor", "Critical"}
