"""EcoNexus AI — Anomaly Intelligence Center."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.layout import page_chrome, global_filters, get_config, empty_state
from ui.cards import (
    kpi_card_compact, section_header, incident_card, insight_card,
)
from ui.charts import trend_line, bar_chart, show
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, BLUE, ORANGE, RED, YELLOW, PURPLE,
    CHART_COLORS, severity_color,
)
from src.anomaly_detection import detect_anomalies

# ── Page shell ───────────────────────────────────────────────────────
page_chrome(
    "Anomaly Intelligence",
    "AI-powered incident detection and investigation",
    "🔍",
)
data, agg = global_filters()
if data.empty:
    st.stop()

settings, thresholds = get_config()

# ── Run detection ────────────────────────────────────────────────────
try:
    with st.spinner("Running anomaly detection engine..."):
        enriched, events, _, metrics = detect_anomalies(
            data, settings["anomaly_contamination"]
        )
except Exception as exc:
    empty_state("⚠️", "Anomaly detection failed", str(exc))
    st.stop()

if events.empty:
    empty_state("✅", "No anomalies detected", "All observations fall within expected ranges.")
    st.stop()

# ── Top metrics strip ────────────────────────────────────────────────
total_anomalies = len(events)
high_count = int((events["severity"].astype(str) == "High").sum())
critical_count = int((events["severity"].astype(str) == "Critical").sum())
anomaly_rate = total_anomalies / len(data) * 100 if len(data) > 0 else 0
precision = metrics.get("precision", 0)
recall = metrics.get("recall", 0)
f1 = metrics.get("f1", 0)

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
with m1:
    kpi_card_compact("Total Anomalies", str(total_anomalies), color=ORANGE)
with m2:
    kpi_card_compact("High Severity", str(high_count), color=ORANGE)
with m3:
    kpi_card_compact("Critical", str(critical_count), color=RED)
with m4:
    kpi_card_compact("Anomaly Rate", f"{anomaly_rate:.1f}%", color=YELLOW)
with m5:
    kpi_card_compact("Precision", f"{precision:.2f}", color=CYAN)
with m6:
    kpi_card_compact("Recall", f"{recall:.2f}", color=CYAN)
with m7:
    kpi_card_compact("F1 Score", f"{f1:.2f}", color=GREEN)

# ── Severity filter ──────────────────────────────────────────────────
sev_options = ["Low", "Medium", "High", "Critical"]
selected_sev = st.multiselect(
    "Filter by Severity",
    sev_options,
    default=["Medium", "High", "Critical"],
    key="ai_sev_filter",
)
filtered_events = events[events["severity"].astype(str).isin(selected_sev)]

# ── Section: Anomaly Timeline ────────────────────────────────────────
section_header(
    "Anomaly Timeline",
    "Energy consumption with detected anomalies overlaid",
    "📡",
)

fig_timeline = go.Figure()
for site in enriched["site"].unique():
    site_data = enriched[enriched["site"] == site]
    fig_timeline.add_trace(
        go.Scatter(
            x=site_data["timestamp"],
            y=site_data["total_energy_kwh"],
            name=site,
            mode="lines",
            line=dict(width=1.2),
            opacity=0.6,
        )
    )

sev_colors = {"Low": CYAN, "Medium": YELLOW, "High": ORANGE, "Critical": RED}
for sev_level in sev_options:
    sev_events = filtered_events[filtered_events["severity"].astype(str) == sev_level]
    if not sev_events.empty:
        fig_timeline.add_trace(
            go.Scatter(
                x=sev_events["timestamp"],
                y=sev_events["total_energy_kwh"],
                name=f"{sev_level} Anomaly",
                mode="markers",
                marker=dict(
                    color=sev_colors.get(sev_level, RED),
                    size=8 if sev_level in ("High", "Critical") else 6,
                    symbol="diamond",
                    line=dict(width=1, color="rgba(0,0,0,0.3)"),
                ),
            )
        )

fig_timeline.update_layout(
    title="Energy Anomaly Timeline",
    height=420,
    xaxis_title="Time",
    yaxis_title="Total Energy (kWh)",
)
show(fig_timeline, key="ai_timeline")

# ── Section: Incident Cards ─────────────────────────────────────────
section_header(
    "Incident Cards",
    f"Top {min(20, len(filtered_events))} detected anomaly events",
    "🚨",
)

display_events = filtered_events.sort_values("anomaly_score", ascending=False).head(20)

cols_per_row = 2
rows = [
    display_events.iloc[i : i + cols_per_row]
    for i in range(0, len(display_events), cols_per_row)
]
for row_events in rows:
    cols = st.columns(cols_per_row)
    for idx, (_, ev) in enumerate(row_events.iterrows()):
        with cols[idx]:
            incident_card(
                severity=str(ev.get("severity", "Medium")),
                title=str(ev.get("affected_metric", "Unknown")).replace("_", " ").title(),
                timestamp=str(ev.get("timestamp", ""))[:19],
                details=[
                    f"Observed: {ev.get('observed_value', 'N/A'):.2f}"
                    if pd.notna(ev.get("observed_value"))
                    else "Observed: N/A",
                    f"Expected: {ev.get('expected_range', 'N/A')}",
                    f"Anomaly Score: {ev.get('anomaly_score', 0):.4f}",
                ],
                action=str(ev.get("suggested_action", "")),
            )

# ── Section: Investigation Panel ────────────────────────────────────
section_header(
    "Investigation Panel",
    "Select an incident for deep-dive analysis",
    "🔬",
)

if not filtered_events.empty:
    event_labels = [
        f"{str(row.get('timestamp', ''))[:16]} — "
        f"{str(row.get('affected_metric', '')).replace('_', ' ').title()} "
        f"({row.get('severity', 'N/A')})"
        for _, row in filtered_events.sort_values(
            "anomaly_score", ascending=False
        ).head(50).iterrows()
    ]
    selected_label = st.selectbox(
        "Select Incident",
        event_labels,
        key="ai_investigate",
    )
    sel_idx = event_labels.index(selected_label)
    sel_event = filtered_events.sort_values(
        "anomaly_score", ascending=False
    ).head(50).iloc[sel_idx]

    inv1, inv2 = st.columns([1, 1])
    with inv1:
        st.html(
            f'<div class="eco-card">'
            f'<div class="eco-label">INCIDENT DETAILS</div>'
            f'<div style="margin-top:0.6rem;font-size:0.88rem;color:{TEXT_SECONDARY};line-height:1.75">'
            f'<b style="color:{TEXT}">Timestamp:</b> {str(sel_event.get("timestamp", ""))[:19]}<br>'
            f'<b style="color:{TEXT}">Anomaly Score:</b> {sel_event.get("anomaly_score", 0):.4f}<br>'
            f'<b style="color:{TEXT}">Affected Metric:</b> {str(sel_event.get("affected_metric", "")).replace("_", " ").title()}<br>'
            f'<b style="color:{TEXT}">Expected Range:</b> {sel_event.get("expected_range", "N/A")}<br>'
            f'<b style="color:{TEXT}">Observed Value:</b> {sel_event.get("observed_value", 0):.2f}<br>'
            f'<b style="color:{TEXT}">Severity:</b> '
            f'<span style="color:{severity_color(str(sel_event.get("severity", "Medium")))}">'
            f'{sel_event.get("severity", "N/A")}</span></div></div>'
        )

    with inv2:
        st.html(
            f'<div class="eco-card">'
            f'<div class="eco-label">ROOT CAUSE ANALYSIS</div>'
            f'<div style="margin-top:0.6rem">'
            f'<div style="font-size:0.78rem;color:{TEXT_MUTED};text-transform:uppercase;'
            f'letter-spacing:0.08em;margin-bottom:0.3rem">Probable Explanation</div>'
            f'<div style="font-size:0.88rem;color:{TEXT_SECONDARY};margin-bottom:0.8rem;line-height:1.45">'
            f'{sel_event.get("probable_explanation", "N/A")}</div>'
            f'<div style="font-size:0.78rem;color:{TEXT_MUTED};text-transform:uppercase;'
            f'letter-spacing:0.08em;margin-bottom:0.3rem">Suggested Action</div>'
            f'<div style="font-size:0.88rem;color:{CYAN};line-height:1.45">'
            f'{sel_event.get("suggested_action", "N/A")}</div></div></div>'
        )

    event_ts = pd.Timestamp(sel_event["timestamp"])
    window_start = event_ts - pd.Timedelta(hours=12)
    window_end = event_ts + pd.Timedelta(hours=12)
    window_data = enriched[
        enriched["timestamp"].between(window_start, window_end)
    ]

    if not window_data.empty:
        affected = str(sel_event.get("affected_metric", "total_energy_kwh"))
        plot_cols = ["total_energy_kwh"]
        if affected != "total_energy_kwh" and affected in window_data.columns:
            plot_cols.append(affected)

        fig_inv = go.Figure()
        for i, col in enumerate(plot_cols):
            fig_inv.add_trace(
                go.Scatter(
                    x=window_data["timestamp"],
                    y=window_data[col],
                    name=col.replace("_", " ").title(),
                    line=dict(color=CHART_COLORS[i], width=2),
                    mode="lines",
                )
            )
        fig_inv.add_vline(
            x=event_ts,
            line_dash="dash",
            line_color=RED,
            annotation_text="Anomaly",
            annotation_font_color=RED,
        )
        fig_inv.update_layout(
            title=f"±12 Hours Around Incident ({str(event_ts)[:16]})",
            height=350,
            xaxis_title="Time",
        )
        show(fig_inv, key="ai_investigation_plot")

# ── Section: Severity Distribution ───────────────────────────────────
section_header(
    "Severity Distribution",
    "Breakdown of detected anomalies by severity level",
    "📊",
)

sev_counts = (
    events["severity"]
    .astype(str)
    .value_counts()
    .reindex(sev_options, fill_value=0)
    .reset_index()
)
sev_counts.columns = ["Severity", "Count"]
sev_counts["Color"] = sev_counts["Severity"].map(sev_colors)

fig_sev = go.Figure(
    go.Bar(
        x=sev_counts["Severity"],
        y=sev_counts["Count"],
        marker_color=sev_counts["Color"].tolist(),
        text=sev_counts["Count"],
        textposition="auto",
    )
)
fig_sev.update_layout(
    title="Anomaly Severity Distribution",
    height=340,
    xaxis_title="Severity",
    yaxis_title="Count",
)
show(fig_sev, key="ai_sev_dist")

# ── Disclaimer ───────────────────────────────────────────────────────
st.caption(
    "Synthetic injected labels enable evaluation metrics but simplify real "
    "operational ambiguity. A detected event is not proof of a fault — "
    "engineering review is always required before remediation."
)
