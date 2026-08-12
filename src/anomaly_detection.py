"""Isolation Forest anomaly detection, enriched event records, and evaluation."""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

FEATURES = [
    "total_energy_kwh",
    "cooling_demand_kw",
    "water_consumption_l",
    "pue",
    "server_utilisation_pct",
    "carbon_emissions_kg",
]


def detect_anomalies(
    data: pd.DataFrame,
    contamination: float = 0.025,
    seed: int = 42,
    model_path: str | Path | None = None,
):
    """Fit an Isolation Forest and return row labels, event details, model, and metrics."""
    if data.empty:
        raise ValueError("Cannot detect anomalies in empty data")
    values = (
        data[FEATURES]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(data[FEATURES].median())
    )
    model = IsolationForest(
        n_estimators=160, contamination=contamination, random_state=seed, n_jobs=-1
    )
    labels = model.fit_predict(values)
    scores = -model.decision_function(values)
    enriched = data.copy()
    enriched["detected_anomaly"] = (labels == -1).astype(int)
    enriched["anomaly_score"] = scores
    anomalous = enriched[enriched["detected_anomaly"] == 1].copy()
    z = (
        (anomalous[FEATURES] - data[FEATURES].median())
        / data[FEATURES].std().replace(0, 1)
    ).abs()
    anomalous["affected_metric"] = z.idxmax(axis=1)
    anomalous["observed_value"] = [
        anomalous.loc[i, m] for i, m in anomalous["affected_metric"].items()
    ]
    anomalous["expected_range"] = anomalous["affected_metric"].map(
        {
            c: f"{data[c].quantile(.05):.2f}–{data[c].quantile(.95):.2f}"
            for c in FEATURES
        }
    )
    rank = anomalous["anomaly_score"].rank(pct=True)
    anomalous["severity"] = pd.cut(
        rank,
        [0, 0.5, 0.8, 0.95, 1],
        labels=["Low", "Medium", "High", "Critical"],
        include_lowest=True,
    )
    anomalous["probable_explanation"] = (
        "Likely contributor: measured value differs materially from the multivariate historical pattern; engineering review is required."
    )
    anomalous["suggested_action"] = anomalous["affected_metric"].map(
        {
            "water_consumption_l": "Inspect cooling water circuit for leakage.",
            "cooling_demand_kw": "Inspect cooling set points and airflow.",
            "pue": "Review cooling and non-IT overhead.",
            "server_utilisation_pct": "Review workload placement.",
            "carbon_emissions_kg": "Review energy use and carbon-aware scheduling.",
            "total_energy_kwh": "Check workload and facility plant.",
        }
    )
    metrics = {}
    if "anomaly_ground_truth" in enriched:
        p, r, f, _ = precision_recall_fscore_support(
            enriched["anomaly_ground_truth"],
            enriched["detected_anomaly"],
            average="binary",
            zero_division=0,
        )
        metrics = {
            "precision": float(p),
            "recall": float(r),
            "f1": float(f),
            "confusion_matrix": confusion_matrix(
                enriched["anomaly_ground_truth"], enriched["detected_anomaly"]
            ).tolist(),
            "detected": int(enriched["detected_anomaly"].sum()),
        }
    if model_path:
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path)
    return enriched, anomalous, model, metrics
