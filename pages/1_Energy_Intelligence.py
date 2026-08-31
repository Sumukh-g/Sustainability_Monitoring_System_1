"""EcoNexus AI — Energy Intelligence page."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from ui.cards import insight_card, kpi_card, section_header, stat_row
from ui.charts import area_stack, scatter, show, sparkline_svg, trend_line
from ui.insights import energy_insights
from ui.layout import empty_state, global_filters, page_chrome
from ui.styles import inject_styles
from ui.theme import CHART_COLORS, pue_status


# ── Helpers ──────────────────────────────────────────────────────────

def _resample(df: pd.DataFrame, agg: str) -> pd.DataFrame:
    """Resample time-series data preserving the site dimension."""
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


# ── Page ─────────────────────────────────────────────────────────────

inject_styles()
page_chrome(
    "Energy Intelligence",
    "Facility energy analysis, composition, and workload efficiency",
    "⚡",
)
df, agg = global_filters()

if df.empty:
    empty_state("⚡", "No energy data available", "Adjust filters to see energy intelligence.")
    st.stop()

ts = _resample(df, agg)

# ── Top KPI strip ────────────────────────────────────────────────────

facility_mwh = df.total_energy_kwh.sum() / 1000
it_mwh = df.it_energy_kwh.sum() / 1000
cool_mwh = df.cooling_energy_kwh.sum() / 1000
cool_share = (
    df.cooling_energy_kwh.sum() / df.total_energy_kwh.sum() * 100
    if df.total_energy_kwh.sum() > 0
    else 0.0
)
avg_pue = df.pue.mean()
pue_label, _ = pue_status(avg_pue)

spark_energy = sparkline_svg(
    df.sort_values("timestamp")
    .groupby(df.timestamp.dt.date)
    .total_energy_kwh.mean()
    .tolist()[-30:]
)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    kpi_card("Facility Energy", f"{facility_mwh:,.1f} MWh", icon="⚡", sparkline_svg=spark_energy)
with k2:
    kpi_card("IT Energy", f"{it_mwh:,.1f} MWh", icon="🖥️")
with k3:
    kpi_card("Cooling Energy", f"{cool_mwh:,.1f} MWh", icon="❄️")
with k4:
    kpi_card(
        "Cooling Share", f"{cool_share:.1f}%", icon="📊",
        status="warning" if cool_share > 35 else "good",
    )
with k5:
    kpi_card("PUE", f"{avg_pue:.2f}", icon="⚙️", status=pue_label.lower())

# ── Energy Pulse ─────────────────────────────────────────────────────

section_header("Energy Pulse", "Current energy status and peak prediction", "📊")

mean_kwh = df.total_energy_kwh.mean()
daily_totals = df.groupby(df.timestamp.dt.date).total_energy_kwh.sum()
daily_max = daily_totals.max()
peak_hour = int(df.groupby(df.timestamp.dt.hour).total_energy_kwh.mean().idxmax())

stat_row([
    ("Mean Energy", f"{mean_kwh:,.0f}", "kWh / hour"),
    ("Daily Maximum", f"{daily_max:,.0f}", "kWh"),
    ("Predicted Peak", f"{peak_hour:02d}:00", "hour"),
    ("Cooling Share", f"{cool_share:.1f}%", "of total"),
])

# ── Energy Composition ───────────────────────────────────────────────

section_header("Energy Composition", "Stacked breakdown of facility energy", "🔋")

comp = ts.groupby("timestamp").sum(numeric_only=True).reset_index()
comp["overhead_kwh"] = (
    comp.total_energy_kwh - comp.it_energy_kwh - comp.cooling_energy_kwh
).clip(lower=0)

fig = area_stack(
    comp, "timestamp",
    ["it_energy_kwh", "cooling_energy_kwh", "overhead_kwh"],
    title="Energy Composition Over Time",
)
show(fig, key="energy_composition")

# ── Workload Efficiency ──────────────────────────────────────────────

section_header("Workload Efficiency", "Computational output vs energy consumption", "⚙️")

col_left, col_right = st.columns(2)

with col_left:
    fig = scatter(
        df, "compute_workload_units", "total_energy_kwh",
        color="external_temperature_c",
        title="Energy vs Workload (coloured by External Temp)",
    )
    show(fig, key="workload_scatter")

with col_right:
    eff = ts.groupby("timestamp").mean(numeric_only=True).reset_index()
    eff["kwh_per_workload"] = eff.total_energy_kwh / eff.compute_workload_units.replace(0, np.nan)
    fig = trend_line(
        eff, "timestamp", "kwh_per_workload",
        title="Energy per Workload Unit (kWh / unit)",
    )
    show(fig, key="energy_per_workload_trend")

# ── PUE Timeline ────────────────────────────────────────────────────

section_header("PUE Timeline", "Power Usage Effectiveness across sites", "📈")

fig = px.line(
    ts, x="timestamp", y="pue", color="site",
    title="PUE Over Time by Site",
    color_discrete_sequence=CHART_COLORS,
)
fig.update_layout(height=340)
fig.update_traces(line_width=1.8)
show(fig, key="pue_timeline")

# ── Efficiency Diagnostics ───────────────────────────────────────────

section_header("Efficiency Diagnostics", "AI-generated energy insights", "🔍")

insights = energy_insights(df)
if insights:
    for ins in insights:
        insight_card(ins["text"], ins["level"])
else:
    insight_card("Energy systems operating within normal parameters.", "info")
