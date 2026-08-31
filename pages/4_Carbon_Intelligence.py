"""EcoNexus AI — Carbon Intelligence page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from ui.cards import insight_card, kpi_card, kpi_card_compact, section_header
from ui.charts import heatmap_strip, scatter, show, sparkline_svg, trend_line
from ui.insights import carbon_insights
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


# ── Page ─────────────────────────────────────────────────────────────

inject_styles()
page_chrome(
    "Carbon Intelligence",
    "Emissions monitoring, grid intensity analysis, and decarbonisation insights",
    "🌱",
)
df, agg = global_filters()

if df.empty:
    empty_state("🌱", "No carbon data available", "Adjust filters to see carbon intelligence.")
    st.stop()

ts = _resample(df, agg)

# ── Top KPI strip ────────────────────────────────────────────────────

total_carbon_t = df.carbon_emissions_kg.sum() / 1000
avg_ci = df.grid_carbon_intensity_g_per_kwh.mean()
avg_cue = df.cue_kg_per_kwh.mean()
avg_renew = df.renewable_energy_pct.mean()

spark_carbon = sparkline_svg(
    df.sort_values("timestamp")
    .groupby(df.timestamp.dt.date)
    .carbon_emissions_kg.mean()
    .tolist()[-30:],
    color=GREEN,
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Carbon", f"{total_carbon_t:,.2f} tCO₂e", icon="🌱", sparkline_svg=spark_carbon)
with k2:
    ci_status = "optimal" if avg_ci < 200 else "warning" if avg_ci < 400 else "critical"
    kpi_card("Carbon Intensity", f"{avg_ci:,.0f} gCO₂/kWh", icon="📊", status=ci_status)
with k3:
    cue_status = "optimal" if avg_cue < 0.3 else "warning" if avg_cue < 0.6 else "critical"
    kpi_card("CUE", f"{avg_cue:.3f}", icon="📐", status=cue_status)
with k4:
    ren_status = "optimal" if avg_renew > 60 else "good" if avg_renew > 30 else "warning"
    kpi_card("Renewable %", f"{avg_renew:.1f}%", icon="♻️", status=ren_status)

# ── Carbon Operations Center ─────────────────────────────────────────

section_header("Carbon Operations Center", "Emissions and grid intensity timeline", "📡")

ts_all = ts.groupby("timestamp").mean(numeric_only=True).reset_index()

fig = trend_line(
    ts_all, "timestamp",
    ["carbon_emissions_kg", "grid_carbon_intensity_g_per_kwh"],
    title="Carbon Emissions & Grid Intensity Over Time",
)
show(fig, key="carbon_operations")

# ── Carbon Intensity Strip ───────────────────────────────────────────

section_header("Carbon Intensity Strip", "24-hour grid carbon intensity profile", "🔥")

hourly_ci = df.groupby(df.timestamp.dt.hour).grid_carbon_intensity_g_per_kwh.mean()
hour_labels = [f"{h:02d}:00" for h in range(24)]
hour_values = [hourly_ci.get(h, 0) for h in range(24)]

fig = heatmap_strip(
    hour_values, hour_labels,
    title="Average Grid Carbon Intensity by Hour (gCO₂/kWh)",
    low_color=GREEN, high_color=RED,
    height=120,
)
show(fig, key="carbon_intensity_heatmap")

low_4 = hourly_ci.nsmallest(4)
low_hours_str = ", ".join(f"{int(h):02d}:00" for h in sorted(low_4.index))
low_avg_val = low_4.mean()

lc1, lc2 = st.columns(2)
with lc1:
    kpi_card_compact(
        "Low-Carbon Window",
        low_hours_str,
        sub=f"Average intensity: {low_avg_val:.0f} gCO₂/kWh during these hours",
        color=GREEN,
    )
with lc2:
    high_4 = hourly_ci.nlargest(4)
    high_hours_str = ", ".join(f"{int(h):02d}:00" for h in sorted(high_4.index))
    high_avg_val = high_4.mean()
    kpi_card_compact(
        "Peak-Carbon Hours",
        high_hours_str,
        sub=f"Average intensity: {high_avg_val:.0f} gCO₂/kWh — avoid flexible loads",
        color=RED,
    )

# ── Energy–Carbon Relationship ───────────────────────────────────────

section_header("Energy–Carbon Relationship", "How energy consumption maps to emissions", "🔗")

fig = scatter(
    df, "total_energy_kwh", "carbon_emissions_kg",
    color="renewable_energy_pct",
    title="Energy vs Carbon Emissions (coloured by Renewable %)",
)
show(fig, key="energy_carbon_scatter")

# ── Renewable Energy Mix ─────────────────────────────────────────────

section_header("Renewable Energy Mix", "Renewable energy proportion over time", "♻️")

fig = trend_line(
    ts_all, "timestamp", "renewable_energy_pct",
    title="Renewable Energy Percentage Over Time",
)
show(fig, key="renewable_energy_trend")

# ── CUE Timeline ────────────────────────────────────────────────────

section_header("CUE Timeline", "Carbon Usage Effectiveness across sites", "📈")

fig = px.line(
    ts, x="timestamp", y="cue_kg_per_kwh", color="site",
    title="CUE Over Time by Site",
    color_discrete_sequence=CHART_COLORS,
)
fig.update_layout(height=340)
fig.update_traces(line_width=1.8)
show(fig, key="cue_timeline")

# ── Carbon Insights ──────────────────────────────────────────────────

section_header("Carbon Insights", "AI-generated decarbonisation insights", "🔍")

insights = carbon_insights(df)

weekly_emissions = df.set_index("timestamp").resample("7D").carbon_emissions_kg.sum()
if len(weekly_emissions) > 1 and weekly_emissions.iloc[0] > 0:
    trend_pct = (weekly_emissions.iloc[-1] - weekly_emissions.iloc[0]) / weekly_emissions.iloc[0] * 100
    if abs(trend_pct) > 5:
        direction = "increase" if trend_pct > 0 else "decrease"
        insights.append({
            "text": f"Weekly carbon emissions show a {abs(trend_pct):.1f}% {direction} over the selected period.",
            "level": "warn" if trend_pct > 0 else "info",
        })

insights.append({
    "text": f"Best hours for carbon-aware scheduling: {low_hours_str} (avg {low_avg_val:.0f} gCO₂/kWh).",
    "level": "info",
})

if insights:
    for ins in insights:
        insight_card(ins["text"], ins["level"])
else:
    insight_card("Carbon metrics are within expected parameters.", "info")
