"""Secure loading and automated quality validation."""

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "timestamp",
    "site",
    "total_energy_kwh",
    "it_energy_kwh",
    "cooling_energy_kwh",
    "water_consumption_l",
    "cooling_demand_kw",
    "carbon_emissions_kg",
    "pue",
    "wue_l_per_kwh",
    "cue_kg_per_kwh",
}


def load_data(
    path: str | Path = "data/generated/data_centre_hourly.csv",
) -> pd.DataFrame:
    """Load a CSV only, validate its schema, and parse timestamps."""
    path = Path(path)
    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV datasets are supported")
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Run python -m src.data_generation"
        )
    data = pd.read_csv(path, low_memory=False)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    return data


def validate_data(data: pd.DataFrame) -> pd.DataFrame:
    """Return machine-readable quality checks; a pass is never fabricated."""
    if data.empty:
        return pd.DataFrame(
            [
                {
                    "check": "non_empty",
                    "passed": False,
                    "count": 1,
                    "detail": "Dataset is empty",
                }
            ]
        )
    numeric = [
        c
        for c in [
            "total_energy_kwh",
            "it_energy_kwh",
            "cooling_energy_kwh",
            "water_consumption_l",
            "cooling_demand_kw",
            "carbon_emissions_kg",
        ]
        if c in data
    ]
    checks = [
        (
            "missing_values",
            int(data.isna().sum().sum()) == 0,
            int(data.isna().sum().sum()),
            "All fields",
        ),
        (
            "duplicate_site_timestamps",
            not data.duplicated(["site", "timestamp"]).any(),
            int(data.duplicated(["site", "timestamp"]).sum()),
            "Unique within site",
        ),
        (
            "negative_consumption",
            not (data[numeric] < 0).any().any(),
            int((data[numeric] < 0).sum().sum()),
            "Energy/water/cooling/carbon",
        ),
        (
            "utilisation_range",
            data["server_utilisation_pct"].between(0, 100).all(),
            int((~data["server_utilisation_pct"].between(0, 100)).sum()),
            "Expected 0–100%",
        ),
        (
            "sensor_range",
            data["external_temperature_c"].between(-30, 60).all(),
            int((~data["external_temperature_c"].between(-30, 60)).sum()),
            "Physical plausibility bound -30–60 C; intentional sensor anomalies remain inside this bound",
        ),
        (
            "sustainability_ratios",
            (data[["pue", "wue_l_per_kwh", "cue_kg_per_kwh"]].ge(0).all().all()),
            int((data[["pue", "wue_l_per_kwh", "cue_kg_per_kwh"]] < 0).sum().sum()),
            "Ratios non-negative",
        ),
    ]
    outlier_columns = numeric + [
        column
        for column in [
            "external_temperature_c",
            "humidity_pct",
            "server_utilisation_pct",
            "pue",
            "wue_l_per_kwh",
            "cue_kg_per_kwh",
        ]
        if column in data and column not in numeric
    ]
    z = (
        (data[outlier_columns] - data[outlier_columns].mean())
        / data[outlier_columns].std().replace(0, 1)
    ).abs()
    extreme = z.gt(6).any(axis=1)
    unexplained = extreme & ~data.get(
        "anomaly_ground_truth", pd.Series(0, index=data.index)
    ).astype(bool)
    checks.append(
        (
            "unexplained_extreme_outliers",
            not unexplained.any(),
            int(unexplained.sum()),
            f"{int(extreme.sum())} extreme rows; labelled injected anomalies are retained",
        )
    )
    for site, group in data.groupby("site"):
        continuity = (
            group["timestamp"]
            .sort_values()
            .diff()
            .dropna()
            .eq(pd.Timedelta(hours=1))
            .all()
        )
        checks.append(
            (
                f"hourly_continuity:{site}",
                continuity,
                int(not continuity),
                "Hourly steps",
            )
        )
    return pd.DataFrame(
        [
            {"check": n, "passed": bool(p), "count": c, "detail": d}
            for n, p, c, d in checks
        ]
    )
