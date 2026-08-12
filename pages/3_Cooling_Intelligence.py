"""EcoNexus AI — Cooling Intelligence page."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from ui.cards import insight_card, kpi_card, section_header
from ui.charts import gauge, scatter, show, sparkline_svg, trend_line
from ui.insights import cooling_insights
from ui.layout import empty_state, global_filters, page_chrome
from ui.styles import inject_styles
from ui.theme import CHART_COLORS, GREEN, ORANGE, RED, YELLOW


# ── Helpers ──────────────────────────────────────────────────────────

def _resample(df: pd.DataFrame, agg: str) -> pd.DataFrame:
    if agg == "Hourly" or df.empty:
        return df
    freq = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}.get(agg, "D")
    num_cols = df.select_dtypes(include="number").columns.tolist()
    return (
        df.set_index("timestamp")
        .groupby("site")[num_cols]
        .resample(freq)
        .mean()
        .reset_index()
    )


def _thermal_stress(ext_temp: pd.Series, cool_eff: pd.Series) -> float:
    """Project-derived thermal stress index (0-100).

    Combines the percentile rank of current external temperature against
    the historical distribution with the inverse of cooling efficiency.
    This is NOT an industry-standard metric.
    """
    if ext_temp.empty or cool_eff.empty:
        return 50.0

    temp_mean = ext_temp.mean()
    temp_pct = (ext_temp > temp_mean).mean() * 100

    eff_mean = cool_eff.mean()
    eff_penalty = max(0, 1 - eff_mean) * 100 if eff_mean > 0 else 50

    return float(np.clip(temp_pct * 0.55 + eff_penalty * 0.45, 0, 100))


# ── Page ─────────────────────────────────────────────────────────────

inject_styles()
page_chrome(
    "Cooling Intelligence",
    "Cooling demand, thermal management, and efficiency diagnostics",
    "❄️",
)
df, agg = global_filters()

if df.empty:
    empty_state("❄️", "No cooling data available", "Adjust filters to see cooling intelligence.")
    st.stop()

ts = _resample(df, agg)

# ── Top KPI strip ────────────────────────────────────────────────────

avg_cooling_kw = df.cooling_demand_kw.mean()
cool_energy_mwh = df.cooling_energy_kwh.sum() / 1000
avg_cool_eff = df.cooling_efficiency.mean()
avg_ext_temp = df.external_temperature_c.mean()

spark_cool = sparkline_svg(
    df.sort_values("timestamp")
    .groupby(df.timestamp.dt.date)
    .cooling_demand_kw.mean()
    .tolist()[-30:]
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Cooling Demand", f"{avg_cooling_kw:,.1f} kW", icon="❄️", sparkline_svg=spark_cool)
with k2:
    kpi_card("Cooling Energy", f"{cool_energy_mwh:,.1f} MWh", icon="🔋")
with k3:
    eff_status = "optimal" if avg_cool_eff > 0.85 else "good" if avg_cool_eff > 0.7 else "warning"
    kpi_card("Cooling Efficiency", f"{avg_cool_eff:.2f}", icon="📐", status=eff_status)
with k4:
    temp_status = "optimal" if avg_ext_temp < 20 else "warning" if avg_ext_temp < 30 else "elevated"
    kpi_card("External Temp", f"{avg_ext_temp:.1f} °C", icon="🌡️", status=temp_status)

# ── Cooling Operations ───────────────────────────────────────────────

section_header("Cooling Operations", "Demand and energy trends with fault markers", "🔄")

ts_all = ts.groupby("timestamp").mean(numeric_only=True).reset_index()
fault_mask = df.anomaly_type == "Cooling fault"
markers = df[fault_mask] if fault_mask.any() else None

fig = trend_line(
    ts_all, "timestamp",
    ["cooling_demand_kw", "cooling_energy_kwh"],
    title="Cooling Demand & Energy",
    markers=markers,
    marker_label="Cooling Fault",
    marker_col="cooling_demand_kw",
)
show(fig, key="cooling_operations")

# ── Thermal Environment ──────────────────────────────────────────────

section_header("Thermal Environment", "External and supply temperature profiles", "🌡️")

fig = trend_line(
    ts_all, "timestamp",
    ["external_temperature_c", "supply_temperature_c"],
    title="Temperature Profiles Over Time",
)
show(fig, key="thermal_environment")

# ── Cooling Relationships ────────────────────────────────────────────

section_header("Cooling Relationships", "Drivers of cooling demand", "🔗")

col_left, col_right = st.columns(2)

with col_left:
    fig = scatter(
        df, "external_temperature_c", "cooling_demand_kw",
        title="External Temperature vs Cooling Demand",
    )
    show(fig, key="temp_vs_cooling")

with col_right:
    fig = scatter(
        df, "it_load_kw", "cooling_demand_kw",
        title="IT Load vs Cooling Demand",
    )
    show(fig, key="itload_vs_cooling")

# ── Thermal Stress Indicator ─────────────────────────────────────────

section_header("Thermal Stress Indicator", "Project-derived composite metric", "🎯")

stress_score = _thermal_stress(df.external_temperature_c, df.cooling_efficiency)

col_gauge, col_info = st.columns([1, 1])

with col_gauge:
    fig = gauge(
        stress_score,
        title="Thermal Stress Index",
        min_val=0, max_val=100,
        thresholds=[(30, GREEN), (60, YELLOW), (80, ORANGE), (100, RED)],
        height=260,
    )
    show(fig, key="thermal_stress_gauge")

with col_info:
    st.markdown("")
    if stress_score < 30:
        insight_card("Thermal stress is LOW — cooling systems are operating comfortably within margins.", "info")
    elif stress_score < 60:
        insight_card("Thermal stress is MODERATE — external conditions are within normal seasonal range.", "info")
    elif stress_score < 80:
        insight_card("Thermal stress is ELEVATED — consider pre-cooling strategies and monitoring cooling headroom.", "warn")
    else:
        insight_card("Thermal stress is HIGH — external heat combined with reduced efficiency may risk thermal throttling.", "crit")
    insight_card(
        "⚠️ <em>Project-derived metric — not an industry standard.</em> Combines external temperature "
        "percentile rank (55% weight) with inverse cooling efficiency (45% weight).",
        "info",
    )

# ── Cooling Insights ─────────────────────────────────────────────────

section_header("Cooling Insights", "AI-generated observations", "🔍")

insights = cooling_insights(df)

if "external_temperature_c" in df.columns and "cooling_demand_kw" in df.columns:
    corr = df[["external_temperature_c", "cooling_demand_kw"]].corr().iloc[0, 1]
    insights.append({
        "text": f"Correlation between external temperature and cooling demand: {corr:.2f}.",
        "level": "info",
    })
    high_temp = df[df.external_temperature_c > df.external_temperature_c.quantile(0.9)]
    if not high_temp.empty:
        avg_cool = high_temp.cooling_demand_kw.mean()
        normal_cool = df.cooling_demand_kw.mean()
        pct_above = (avg_cool - normal_cool) / normal_cool * 100 if normal_cool > 0 else 0
        insights.append({
            "text": f"During high-temperature periods (>90th pct), cooling demand rises {pct_above:.1f}% above average.",
            "level": "warn" if pct_above > 20 else "info",
        })

fault_count = int(fault_mask.sum()) if fault_mask is not None else 0
if fault_count > 0:
    insights.append({
        "text": f"{fault_count} cooling-fault anomalies detected in the selected period.",
        "level": "crit" if fault_count > 5 else "warn",
    })

if insights:
    for ins in insights:
        insight_card(ins["text"], ins["level"])
else:
    insight_card("Cooling systems operating within normal parameters.", "info")

# ── Cooling Efficiency Trend ─────────────────────────────────────────

section_header("Cooling Efficiency Trend", "Efficiency over time by site", "📈")

fig = px.line(
    ts, x="timestamp", y="cooling_efficiency", color="site",
    title="Cooling Efficiency Over Time by Site",
    color_discrete_sequence=CHART_COLORS,
)
fig.update_layout(height=340)
fig.update_traces(line_width=1.8)
show(fig, key="cooling_efficiency_trend")
