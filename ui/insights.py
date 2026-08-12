"""EcoNexus AI — Automated data-driven insight generation."""

from __future__ import annotations
import pandas as pd
import numpy as np


def generate_operations_brief(data: pd.DataFrame) -> list[dict]:
    """Generate concise operational insights from telemetry. Returns list of {text, level}."""
    if data.empty:
        return [{"text": "No telemetry data available for the selected period.", "level": "warn"}]

    insights: list[dict] = []

    # Energy insights
    if "total_energy_kwh" in data.columns:
        e = data.total_energy_kwh
        mean_e = e.mean()
        last_24h = data.sort_values("timestamp").tail(24)
        if len(last_24h) > 12:
            recent_mean = last_24h.total_energy_kwh.mean()
            diff_pct = (recent_mean - mean_e) / mean_e * 100
            if abs(diff_pct) > 5:
                direction = "above" if diff_pct > 0 else "below"
                insights.append({
                    "text": f"Recent energy consumption is {abs(diff_pct):.1f}% {direction} the period baseline ({mean_e:.0f} kWh).",
                    "level": "warn" if diff_pct > 10 else "info",
                })

        # Peak prediction
        if "timestamp" in data.columns:
            peak_hour = data.groupby(data.timestamp.dt.hour).total_energy_kwh.mean().idxmax()
            insights.append({
                "text": f"Energy demand typically peaks around {peak_hour:02d}:00 based on historical patterns.",
                "level": "info",
            })

    # Cooling insights
    if "cooling_demand_kw" in data.columns and "total_energy_kwh" in data.columns:
        cool_share = data.cooling_demand_kw.sum() / data.total_energy_kwh.sum() * 100
        insights.append({
            "text": f"Cooling accounts for {cool_share:.1f}% of total facility energy in this period.",
            "level": "warn" if cool_share > 35 else "info",
        })

    # Water insights
    if "water_consumption_l" in data.columns:
        w = data.water_consumption_l
        q75 = w.quantile(0.75)
        outliers = (w > q75 * 1.5).sum()
        if outliers > 0:
            insights.append({
                "text": f"{outliers} water consumption readings exceed 1.5× the 75th percentile — potential anomalies.",
                "level": "warn",
            })
        else:
            insights.append({
                "text": "Water consumption remains within normal operating range.",
                "level": "info",
            })

    # Carbon insights
    if "grid_carbon_intensity_g_per_kwh" in data.columns:
        ci = data.grid_carbon_intensity_g_per_kwh
        low_hours = data[ci < ci.quantile(0.25)].timestamp.dt.hour.mode()
        if len(low_hours) > 0:
            h = int(low_hours.iloc[0])
            insights.append({
                "text": f"Lowest carbon intensity typically occurs around {h:02d}:00 — a potential window for flexible workloads.",
                "level": "info",
            })

    # PUE insights
    if "pue" in data.columns:
        pue_median = data.pue.median()
        pue_last = data.sort_values("timestamp").tail(24).pue.median()
        diff = pue_last - pue_median
        if abs(diff) > 0.03:
            direction = "higher" if diff > 0 else "lower"
            insights.append({
                "text": f"Recent PUE ({pue_last:.2f}) is {abs(diff):.2f} {direction} than the period median ({pue_median:.2f}).",
                "level": "warn" if diff > 0 else "info",
            })

    # Anomaly summary
    if "anomaly_flag" in data.columns:
        anom_count = int(data.anomaly_flag.sum())
        if anom_count > 0:
            insights.append({
                "text": f"{anom_count} anomalous observations detected in the selected period requiring review.",
                "level": "crit" if anom_count > 20 else "warn",
            })
        else:
            insights.append({
                "text": "No anomalies detected in the selected period.",
                "level": "info",
            })

    return insights


def energy_insights(data: pd.DataFrame) -> list[dict]:
    """Energy-specific diagnostic insights."""
    insights = []
    if data.empty:
        return insights

    if "cooling_demand_kw" in data.columns and "total_energy_kwh" in data.columns:
        cool_pct = data.cooling_demand_kw.sum() / data.total_energy_kwh.sum() * 100
        weekly = data.set_index("timestamp").resample("7D").cooling_demand_kw.mean()
        if len(weekly) > 1:
            trend = (weekly.iloc[-1] - weekly.iloc[0]) / (weekly.iloc[0] + 1e-9) * 100
            if abs(trend) > 5:
                direction = "increase" if trend > 0 else "decrease"
                insights.append({
                    "text": f"Cooling overhead shows a {abs(trend):.1f}% {direction} over the period.",
                    "level": "warn" if trend > 0 else "info",
                })

    if "server_utilisation_pct" in data.columns:
        util = data.server_utilisation_pct.mean()
        insights.append({
            "text": f"Average server utilisation is {util:.1f}%.",
            "level": "warn" if util < 40 else "info",
        })

    if "total_energy_kwh" in data.columns and "timestamp" in data.columns:
        hourly = data.groupby(data.timestamp.dt.hour).total_energy_kwh.mean()
        peak_start = hourly.rolling(4).mean().idxmax() - 2
        peak_end = peak_start + 4
        insights.append({
            "text": f"Peak energy consumption typically occurs between {max(0,peak_start):02d}:00–{min(23,peak_end):02d}:00.",
            "level": "info",
        })

    return insights


def carbon_insights(data: pd.DataFrame) -> list[dict]:
    """Carbon-specific insights."""
    insights = []
    if data.empty or "grid_carbon_intensity_g_per_kwh" not in data.columns:
        return insights

    ci = data.grid_carbon_intensity_g_per_kwh
    hourly_ci = data.groupby(data.timestamp.dt.hour).grid_carbon_intensity_g_per_kwh.mean()
    low_hours = hourly_ci.nsmallest(4).index.tolist()
    low_hours_str = ", ".join(f"{h:02d}:00" for h in sorted(low_hours))
    insights.append({
        "text": f"Lowest carbon intensity hours: {low_hours_str} — consider scheduling flexible loads here.",
        "level": "info",
    })

    if "renewable_energy_pct" in data.columns:
        ren = data.renewable_energy_pct.mean()
        insights.append({
            "text": f"Average renewable energy proportion: {ren:.1f}%.",
            "level": "info" if ren > 30 else "warn",
        })

    return insights


def cooling_insights(data: pd.DataFrame) -> list[dict]:
    """Cooling-specific insights."""
    insights = []
    if data.empty:
        return insights

    if "external_temp_c" in data.columns and "cooling_demand_kw" in data.columns:
        corr = data[["external_temp_c", "cooling_demand_kw"]].corr().iloc[0, 1]
        insights.append({
            "text": f"Correlation between external temperature and cooling demand: {corr:.2f}.",
            "level": "info",
        })

        high_temp = data[data.external_temp_c > data.external_temp_c.quantile(0.9)]
        if not high_temp.empty:
            avg_cool = high_temp.cooling_demand_kw.mean()
            normal_cool = data.cooling_demand_kw.mean()
            pct_above = (avg_cool - normal_cool) / normal_cool * 100
            insights.append({
                "text": f"During high-temperature periods (>90th pct), cooling demand rises {pct_above:.1f}% above average.",
                "level": "warn" if pct_above > 20 else "info",
            })

    return insights
