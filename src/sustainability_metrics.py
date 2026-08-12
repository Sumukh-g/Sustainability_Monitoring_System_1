"""Recognised sustainability KPIs and the project-specific composite score."""

from __future__ import annotations

import numpy as np
import pandas as pd


def safe_ratio(numerator, denominator):
    """Divide while returning NaN for missing, zero, or negative denominators."""
    scalar = np.isscalar(numerator) and np.isscalar(denominator)
    n = pd.Series([numerator] if scalar else numerator, dtype="float64")
    d = pd.Series([denominator] if scalar else denominator, dtype="float64")
    result = n.div(d.where(d > 0)).replace([np.inf, -np.inf], np.nan)
    return float(result.iloc[0]) if scalar else result


def calculate_pue(facility_energy_kwh, it_energy_kwh):
    """Power Usage Effectiveness: facility kWh / IT kWh (dimensionless)."""
    return safe_ratio(facility_energy_kwh, it_energy_kwh)


def calculate_wue(water_l, it_energy_kwh):
    """Site Water Usage Effectiveness: water litres / IT kWh."""
    return safe_ratio(water_l, it_energy_kwh)


def calculate_cue(carbon_kg, it_energy_kwh):
    """Carbon Usage Effectiveness: location-based kg CO2e / IT kWh."""
    return safe_ratio(carbon_kg, it_energy_kwh)


def add_sustainability_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with PUE, WUE, CUE, and energy/workload indicators."""
    result = df.copy()
    result["pue"] = calculate_pue(result["total_energy_kwh"], result["it_energy_kwh"])
    result["wue_l_per_kwh"] = calculate_wue(
        result["water_consumption_l"], result["it_energy_kwh"]
    )
    result["cue_kg_per_kwh"] = calculate_cue(
        result["carbon_emissions_kg"], result["it_energy_kwh"]
    )
    result["energy_per_workload_kwh"] = safe_ratio(
        result["total_energy_kwh"], result["compute_workload_units"]
    )
    return result


def sustainability_score(
    df: pd.DataFrame, weights: dict[str, float] | None = None
) -> tuple[float, str]:
    """Calculate a transparent 0–100 project indicator (not an industry standard)."""
    weights = weights or {
        "pue": 0.25,
        "wue": 0.20,
        "carbon": 0.20,
        "cooling": 0.15,
        "utilisation": 0.10,
        "anomalies": 0.10,
    }
    mean = df.mean(numeric_only=True)
    parts = {
        "pue": np.clip((2.0 - mean.get("pue", 2.0)) / 0.8, 0, 1),
        "wue": np.clip((2.5 - mean.get("wue_l_per_kwh", 2.5)) / 2, 0, 1),
        "carbon": np.clip((0.6 - mean.get("cue_kg_per_kwh", 0.6)) / 0.5, 0, 1),
        "cooling": np.clip(mean.get("cooling_efficiency", 0) / 5, 0, 1),
        "utilisation": np.clip(mean.get("server_utilisation_pct", 0) / 80, 0, 1),
        "anomalies": 1
        - np.clip(
            mean.get("detected_anomaly", mean.get("anomaly_ground_truth", 0)) * 10, 0, 1
        ),
    }
    denominator = sum(weights.get(key, 0) for key in parts) or 1
    score = float(
        np.clip(
            100 * sum(parts[key] * weights.get(key, 0) for key in parts) / denominator,
            0,
            100,
        )
    )
    label = (
        "Excellent"
        if score >= 85
        else (
            "Good"
            if score >= 70
            else "Moderate" if score >= 50 else "Poor" if score >= 30 else "Critical"
        )
    )
    return score, label
