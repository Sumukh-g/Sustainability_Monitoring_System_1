"""Configuration-driven alerts."""

import pandas as pd


def active_alerts(data: pd.DataFrame, thresholds: dict) -> list[str]:
    if data.empty:
        return ["No data in selected range"]
    latest = data.sort_values("timestamp").iloc[-1]
    alerts = []
    if latest.pue > thresholds["pue_warning"]:
        alerts.append(f"PUE {latest.pue:.2f} exceeds {thresholds['pue_warning']:.2f}")
    if latest.wue_l_per_kwh > thresholds["wue_warning_l_per_kwh"]:
        alerts.append(f"WUE {latest.wue_l_per_kwh:.2f} L/kWh is elevated")
    if (
        latest.grid_carbon_intensity_g_per_kwh
        > thresholds["carbon_intensity_high_g_per_kwh"]
    ):
        alerts.append("Grid carbon intensity is high")
    history = data.sort_values("timestamp").iloc[:-1]
    if not history.empty:
        for column, label in [
            ("total_energy_kwh", "Facility energy"),
            ("water_consumption_l", "Water consumption"),
            ("cooling_demand_kw", "Cooling demand"),
        ]:
            reference = history[column].quantile(thresholds["energy_peak_percentile"])
            if latest[column] > reference:
                alerts.append(
                    f"{label} exceeds its historical "
                    f"{thresholds['energy_peak_percentile']:.0%} reference"
                )
    if latest.get("detected_anomaly", 0):
        alerts.append("AI anomaly detected at latest observation")
    return alerts
