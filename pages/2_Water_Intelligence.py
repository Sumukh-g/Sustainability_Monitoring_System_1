"""EcoNexus AI — Water Intelligence page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from ui.cards import (
    insight_card,
    kpi_card,
    kpi_card_compact,
    section_header,
)
from ui.charts import scatter, show, sparkline_svg, trend_line
from ui.layout import empty_state, global_filters, page_chrome
from ui.styles import inject_styles
from ui.theme import CHART_COLORS, CYAN, GREEN, ORANGE, RED, YELLOW


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


def _water_risk(wue: float, anomaly_count: int) -> tuple[str, str, str]:
    """Return (level_label, status_key, description) for water risk."""
    if anomaly_count > 5 or wue > 2.5:
        return "HIGH", "critical", "Multiple water anomalies detected with elevated WUE — immediate investigation recommended."
    if anomaly_count > 2 or wue > 1.8:
        return "ELEVATED", "elevated", "Water efficiency metrics are above ideal thresholds — monitor closely."
    if anomaly_count > 0 or wue > 1.2:
        return "MODERATE", "warning", "Minor water irregularities detected — within acceptable operational range."
    return "LOW", "optimal", "Water operations are within optimal parameters across all metrics."


# ── Page ─────────────────────────────────────────────────────────────

inject_styles()
page_chrome(
    "Water Intelligence",
    "Water operations, efficiency metrics, and risk assessment",
    "💧",
)
df, agg = global_filters()

if df.empty:
    empty_state("💧", "No water data available", "Adjust filters to see water intelligence.")
    st.stop()

ts = _resample(df, agg)

# ── Top KPI strip ────────────────────────────────────────────────────

total_water_kl = df.water_consumption_l.sum() / 1000
cooling_water_kl = df.cooling_water_l.sum() / 1000
avg_wue = df.wue_l_per_kwh.mean()
water_anomalies = int((df.anomaly_type == "Water leak").sum())

spark_water = sparkline_svg(
    df.sort_values("timestamp")
    .groupby(df.timestamp.dt.date)
    .water_consumption_l.mean()
    .tolist()[-30:],
    color=CYAN,
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Water", f"{total_water_kl:,.1f} kL", icon="💧", sparkline_svg=spark_water)
with k2:
    kpi_card("Cooling Water", f"{cooling_water_kl:,.1f} kL", icon="🌊")
with k3:
    wue_status = "optimal" if avg_wue < 1.2 else "warning" if avg_wue < 1.8 else "critical"
    kpi_card("WUE", f"{avg_wue:.2f} L/kWh", icon="📐", status=wue_status)
with k4:
    anom_status = "optimal" if water_anomalies == 0 else "warning" if water_anomalies <= 3 else "critical"
    kpi_card("Water Anomalies", str(water_anomalies), icon="⚠️", status=anom_status)

# ── Water Operations ─────────────────────────────────────────────────

section_header("Water Operations", "Consumption trends with anomaly markers", "🔄")

ts_all = ts.groupby("timestamp").mean(numeric_only=True).reset_index()
anomaly_mask = df.anomaly_type == "Water leak"
markers = df[anomaly_mask] if anomaly_mask.any() else None

fig = trend_line(
    ts_all, "timestamp",
    ["water_consumption_l", "cooling_water_l"],
    title="Water Consumption & Cooling Water",
    markers=markers,
    marker_label="Water Leak",
    marker_col="water_consumption_l",
)
show(fig, key="water_operations")

# ── Water Efficiency ─────────────────────────────────────────────────

section_header("Water Efficiency", "Water Usage Effectiveness across sites", "📈")

fig = px.line(
    ts, x="timestamp", y="wue_l_per_kwh", color="site",
    title="WUE Over Time by Site",
    color_discrete_sequence=CHART_COLORS,
)
fig.update_layout(height=340)
fig.update_traces(line_width=1.8)
show(fig, key="wue_timeline")

# ── Water Relationships ──────────────────────────────────────────────

section_header("Water Relationships", "Correlations between water usage and operating conditions", "🔗")

col_left, col_right = st.columns(2)

with col_left:
    fig = scatter(
        df, "cooling_demand_kw", "water_consumption_l",
        color="external_temperature_c",
        title="Cooling Demand vs Water Consumption",
    )
    show(fig, key="water_vs_cooling")

with col_right:
    fig = scatter(
        df, "external_temperature_c", "water_consumption_l",
        title="External Temperature vs Water Consumption",
    )
    show(fig, key="water_vs_temp")

# ── Water Risk Assessment ────────────────────────────────────────────

section_header("Water Risk Assessment", "Operational risk based on WUE and anomaly frequency", "🛡️")

risk_label, risk_status, risk_desc = _water_risk(avg_wue, water_anomalies)

r1, r2, r3 = st.columns(3)
with r1:
    kpi_card_compact("Risk Level", risk_label, sub=risk_desc, color={
        "critical": RED, "elevated": ORANGE, "warning": YELLOW, "optimal": GREEN,
    }.get(risk_status, GREEN))
with r2:
    cooling_ratio = cooling_water_kl / total_water_kl * 100 if total_water_kl > 0 else 0
    kpi_card_compact("Cooling Water Ratio", f"{cooling_ratio:.1f}%", sub="Proportion used for cooling")
with r3:
    wue_std = df.wue_l_per_kwh.std()
    kpi_card_compact("WUE Variability", f"σ = {wue_std:.3f}", sub="Standard deviation of WUE")

# ── Water Insights ───────────────────────────────────────────────────

section_header("Water Insights", "AI-generated observations", "🔍")

water_insights: list[dict] = []

q75 = df.water_consumption_l.quantile(0.75)
outliers = int((df.water_consumption_l > q75 * 1.5).sum())
if outliers > 0:
    water_insights.append({
        "text": f"{outliers} water consumption readings exceed 1.5× the 75th percentile — potential anomalies worth investigating.",
        "level": "warn",
    })
else:
    water_insights.append({
        "text": "Water consumption remains within normal operating range throughout the selected period.",
        "level": "info",
    })

if water_anomalies > 0:
    water_insights.append({
        "text": f"{water_anomalies} water-leak anomalies detected. Review cooling loop integrity and valve sensors.",
        "level": "crit" if water_anomalies > 5 else "warn",
    })

corr = df[["external_temperature_c", "water_consumption_l"]].corr().iloc[0, 1]
water_insights.append({
    "text": f"Correlation between external temperature and water consumption: {corr:.2f}.",
    "level": "info",
})

weekly = df.set_index("timestamp").resample("7D").water_consumption_l.mean()
if len(weekly) > 1 and weekly.iloc[0] > 0:
    trend_pct = (weekly.iloc[-1] - weekly.iloc[0]) / weekly.iloc[0] * 100
    if abs(trend_pct) > 5:
        direction = "upward" if trend_pct > 0 else "downward"
        water_insights.append({
            "text": f"Water consumption shows a {abs(trend_pct):.1f}% {direction} trend over the selected period.",
            "level": "warn" if trend_pct > 10 else "info",
        })

for ins in water_insights:
    insight_card(ins["text"], ins["level"])
