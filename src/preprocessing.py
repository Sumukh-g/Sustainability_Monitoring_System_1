"""Leakage-aware cleaning and chronological splitting."""

import pandas as pd


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Parse/deduplicate/order records and impute numeric values within each site."""
    if data.empty:
        return data.copy()
    result = data.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], errors="coerce")
    result = (
        result.dropna(subset=["timestamp"])
        .drop_duplicates(["site", "timestamp"])
        .sort_values(["site", "timestamp"])
    )
    numeric = result.select_dtypes("number").columns
    result[numeric] = result.groupby("site")[numeric].transform(
        lambda x: x.interpolate(limit_direction="both")
    )
    for col in [
        c
        for c in numeric
        if any(term in c for term in ("energy", "water", "load", "emissions"))
    ]:
        result[col] = result[col].clip(lower=0)
    if "server_utilisation_pct" in result:
        result["server_utilisation_pct"] = result["server_utilisation_pct"].clip(0, 100)
    return result.reset_index(drop=True)


def chronological_split(
    data: pd.DataFrame, train_fraction: float = 0.70, validation_fraction: float = 0.15
):
    """Split sorted observations without shuffling; return train, validation, test."""
    if (
        not 0 < train_fraction < 1
        or not 0 <= validation_fraction < 1
        or train_fraction + validation_fraction >= 1
    ):
        raise ValueError("Invalid split fractions")
    ordered = data.sort_values("timestamp")
    n = len(ordered)
    a, b = int(n * train_fraction), int(n * (train_fraction + validation_fraction))
    return ordered.iloc[:a].copy(), ordered.iloc[a:b].copy(), ordered.iloc[b:].copy()
