"""Reproducible, causally related synthetic data-centre time series."""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from src.sustainability_metrics import add_sustainability_metrics

OUTPUT = Path("data/generated/data_centre_hourly.csv")


def generate_data(
    periods: int = 8784,
    seed: int = 42,
    sites: tuple[str, ...] = ("London-DC1", "Manchester-DC2"),
) -> pd.DataFrame:
    """Generate hourly measurements with seasonal, workload, physical, and fault relationships."""
    rng = np.random.default_rng(seed)
    frames = []
    timestamps = pd.date_range("2024-01-01", periods=periods, freq="h")
    for site_number, site in enumerate(sites):
        hour = timestamps.hour.to_numpy()
        dayofyear = timestamps.dayofyear.to_numpy()
        weekday = timestamps.dayofweek.to_numpy()
        daily = np.sin(2 * np.pi * (hour - 8) / 24)
        seasonal = np.sin(2 * np.pi * (dayofyear - 172) / 365.25)
        external_temp = (
            12 + 9 * seasonal + 3 * daily + rng.normal(0, 1.7, periods) - site_number
        )
        humidity = np.clip(68 - 0.7 * external_temp + rng.normal(0, 5, periods), 25, 95)
        business = ((weekday < 5) & (hour >= 8) & (hour < 19)).astype(float)
        it_load = np.clip(
            430
            + 125 * business
            + 55 * daily
            + 25 * site_number
            + rng.normal(0, 22, periods),
            250,
            720,
        )
        server_util = np.clip(18 + it_load / 8 + rng.normal(0, 3, periods), 10, 98)
        active_servers = np.rint(210 + it_load * 0.45).astype(int)
        workload = it_load * (1.2 + server_util / 100) + rng.normal(0, 20, periods)
        it_energy = it_load * (0.92 + rng.normal(0, 0.015, periods))
        cooling_demand = np.maximum(
            70,
            0.38 * it_load
            + 8 * np.maximum(external_temp - 16, 0)
            + rng.normal(0, 10, periods),
        )
        cooling_efficiency = np.clip(
            4.2
            - 0.035 * np.maximum(external_temp - 18, 0)
            + rng.normal(0, 0.12, periods),
            2.0,
            5.0,
        )
        cooling_energy = cooling_demand / cooling_efficiency
        cooling_load = 100 * cooling_demand / 450
        non_it = 45 + 0.02 * it_load + rng.normal(0, 3, periods)
        facility = it_energy + cooling_energy + non_it
        water_cooling = np.maximum(
            0,
            cooling_demand * (0.52 + 0.012 * np.maximum(external_temp, 0))
            + rng.normal(0, 9, periods),
        )
        water = water_cooling + 18 + rng.normal(0, 3, periods)
        carbon_intensity = np.clip(
            255
            + 55 * np.sin(2 * np.pi * (hour - 17) / 24)
            + 25 * seasonal
            + rng.normal(0, 18, periods),
            90,
            480,
        )
        renewable = np.clip(
            35 - 0.08 * (carbon_intensity - 250) + rng.normal(0, 4, periods), 5, 75
        )
        carbon = facility * carbon_intensity / 1000
        maintenance = np.zeros(periods, dtype=int)
        anomaly = np.zeros(periods, dtype=int)
        anomaly_type = np.full(periods, "Normal", dtype=object)
        n = max(12, periods // 240)
        candidates = rng.choice(np.arange(168, periods), size=n * 4, replace=False)
        for kind, indices in zip(
            ("Workload spike", "Cooling fault", "Water leak", "Sensor fault"),
            np.array_split(candidates, 4),
        ):
            anomaly[indices] = 1
            anomaly_type[indices] = kind
            if kind == "Workload spike":
                it_energy[indices] *= 1.45
                facility[indices] += it_energy[indices] * 0.25
            elif kind == "Cooling fault":
                cooling_efficiency[indices] *= 0.55
                cooling_energy[indices] *= 1.7
                facility[indices] += cooling_energy[indices] * 0.7
            elif kind == "Water leak":
                water[indices] *= 2.6
            else:
                external_temp[indices] += 25
        maintenance[
            rng.choice(periods, size=max(5, periods // 1000), replace=False)
        ] = 1
        carbon = facility * carbon_intensity / 1000
        frame = pd.DataFrame(
            {
                "timestamp": timestamps,
                "site": site,
                "external_temperature_c": external_temp,
                "humidity_pct": humidity,
                "it_load_kw": it_load,
                "server_utilisation_pct": server_util,
                "active_servers": active_servers,
                "compute_workload_units": workload,
                "it_energy_kwh": it_energy,
                "facility_energy_kwh": facility,
                "total_energy_kwh": facility,
                "cooling_energy_kwh": cooling_energy,
                "water_consumption_l": water,
                "cooling_water_l": water_cooling,
                "cooling_demand_kw": cooling_demand,
                "cooling_system_load_pct": cooling_load,
                "cooling_efficiency": cooling_efficiency,
                "supply_temperature_c": 18 + rng.normal(0, 0.35, periods),
                "return_temperature_c": 25
                + cooling_load / 30
                + rng.normal(0, 0.45, periods),
                "grid_carbon_intensity_g_per_kwh": carbon_intensity,
                "carbon_emissions_kg": carbon,
                "renewable_energy_pct": renewable,
                "maintenance_indicator": maintenance,
                "anomaly_ground_truth": anomaly,
                "anomaly_type": anomaly_type,
            }
        )
        frame["operational_alert_indicator"] = anomaly
        frame["system_status"] = np.where(
            anomaly == 1, "Alert", np.where(maintenance == 1, "Maintenance", "Normal")
        )
        frames.append(frame)
    result = pd.concat(frames, ignore_index=True)
    ts = result["timestamp"]
    result["date"] = ts.dt.date.astype(str)
    result["hour"] = ts.dt.hour
    result["day_of_week"] = ts.dt.day_name()
    result["month"] = ts.dt.month
    result["weekend_indicator"] = (ts.dt.dayofweek >= 5).astype(int)
    result["season"] = result["month"].map(
        {
            12: "Winter",
            1: "Winter",
            2: "Winter",
            3: "Spring",
            4: "Spring",
            5: "Spring",
            6: "Summer",
            7: "Summer",
            8: "Summer",
            9: "Autumn",
            10: "Autumn",
            11: "Autumn",
        }
    )
    return (
        add_sustainability_metrics(result)
        .sort_values(["timestamp", "site"])
        .reset_index(drop=True)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--periods", type=int, default=8784)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = generate_data(args.periods)
    data.to_csv(args.output, index=False)
    print(f"Generated {len(data):,} rows at {args.output}")


if __name__ == "__main__":
    main()
