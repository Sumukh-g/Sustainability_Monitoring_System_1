"""Past-only time-series feature construction."""

import numpy as np
import pandas as pd


def create_features(
    data: pd.DataFrame, target: str = "total_energy_kwh", drop_missing: bool = True
) -> pd.DataFrame:
    """Build time/cyclic, lag, and shifted rolling features independently by site."""
    if target not in data:
        raise ValueError(f"Unknown target: {target}")
    result = data.copy().sort_values(["site", "timestamp"])
    ts = pd.to_datetime(result["timestamp"])
    result["hour"] = ts.dt.hour
    result["weekday"] = ts.dt.dayofweek
    result["month"] = ts.dt.month
    result["weekend"] = (result["weekday"] >= 5).astype(int)
    result["hour_sin"] = np.sin(2 * np.pi * result["hour"] / 24)
    result["hour_cos"] = np.cos(2 * np.pi * result["hour"] / 24)
    result["month_sin"] = np.sin(2 * np.pi * (result["month"] - 1) / 12)
    result["month_cos"] = np.cos(2 * np.pi * (result["month"] - 1) / 12)
    grouped = result.groupby("site", group_keys=False)[target]
    for lag in (1, 24, 48, 168):
        result[f"{target}_lag_{lag}"] = grouped.shift(lag)
    past = grouped.shift(1)
    for window in (3, 6, 24, 168):
        roll = past.groupby(result["site"]).rolling(window, min_periods=window)
        result[f"{target}_roll_mean_{window}"] = roll.mean().reset_index(
            level=0, drop=True
        )
        result[f"{target}_roll_std_{window}"] = roll.std().reset_index(
            level=0, drop=True
        )
        result[f"{target}_roll_min_{window}"] = roll.min().reset_index(
            level=0, drop=True
        )
        result[f"{target}_roll_max_{window}"] = roll.max().reset_index(
            level=0, drop=True
        )
    # Restore global chronology after site-local transforms so downstream splits
    # hold out the latest period across every site, rather than an entire site.
    result = result.sort_values(["timestamp", "site"])
    return result.dropna().reset_index(drop=True) if drop_missing else result
