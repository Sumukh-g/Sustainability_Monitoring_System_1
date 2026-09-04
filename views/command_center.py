"""EcoNexus AI — Command Center (Executive Landing Page)."""

import streamlit as st

import pandas as pd
import numpy as np

from ui.styles import inject_styles
from ui.layout import (
    page_chrome, global_filters, get_data, get_config, empty_state,
    PRODUCT_NAME, PRODUCT_SUBTITLE,
)
from ui.theme import (
    BG_CARD, BG_DARK, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, GREEN_DIM, GREEN_GLOW, CYAN, BLUE, RED, ORANGE, YELLOW,
    score_color, score_label, severity_color, pue_status,
)
from ui.cards import (
    kpi_card, site_card, alert_strip, insight_card, section_header,
    stat_row, kpi_card_compact,
)
from ui.charts import (
    trend_line, sparkline_svg, gauge, show, heatmap_strip,
)
from ui.gauges import sustainability_gauge, efficiency_mini_gauge, pue_gauge
from ui.insights import generate_operations_brief
from src.sustainability_metrics import sustainability_score
from src.alerts import active_alerts

# ── Page shell ──────────────────────────────────────────────────────
inject_styles()

with st.sidebar:
    st.html(
        f'<div style="text-align:center;padding:0.45rem 0 0.7rem 0">'
        f'<div style="font-size:1.25rem;font-weight:800;color:{GREEN};letter-spacing:0.05em">{PRODUCT_NAME}</div>'
        f'<div style="font-size:0.7rem;color:{TEXT_SECONDARY};letter-spacing:0.06em;'
        f'text-transform:uppercase;margin-top:0.2rem;line-height:1.35">{PRODUCT_SUBTITLE}</div></div>'
    )
    st.markdown("---")

data, agg = global_filters(show_aggregation=False)
settings, thresholds = get_config()

if data.empty:
    empty_state("📡", "No telemetry data", "Adjust filters to view operational data.")
    st.stop()

# ── Compute core metrics ────────────────────────────────────────────
score, label = sustainability_score(data, settings["sustainability_score_weights"])
sites = sorted(data.site.unique())
latest = data.sort_values("timestamp").iloc[-1]
alerts = active_alerts(data, thresholds)
mean_vals = data.mean(numeric_only=True)

# ── Command bar ─────────────────────────────────────────────────────
st.html(
    f'<div style="padding:0.15rem 0 0.85rem 0">'
    f'<div style="font-size:clamp(1.3rem,2.1vw,1.65rem);font-weight:800;color:{TEXT};'
    f'letter-spacing:-0.01em;line-height:1.2">Command Center</div>'
    f'<div style="font-size:0.85rem;color:{TEXT_SECONDARY};margin-top:0.3rem;line-height:1.4">'
    f'{PRODUCT_SUBTITLE} for AI Data Centres</div></div>'
)

cb1, cb2, cb3 = st.columns(3)
with cb1:
    site_str = " · ".join(sites)
    st.html(
        f'<div class="eco-card" style="padding:0.85rem 1rem;min-height:4.8rem">'
        f'<div class="eco-label">Active Sites</div>'
        f'<div class="eco-value-sm" style="font-size:0.95rem;line-height:1.4">{site_str}</div></div>'
    )
with cb2:
    ts = latest.timestamp
    ts_str = ts.strftime("%Y-%m-%d %H:%M") if hasattr(ts, "strftime") else str(ts)
    st.html(
        f'<div class="eco-card" style="padding:0.85rem 1rem;min-height:4.8rem">'
        f'<div class="eco-label">Last Telemetry</div>'
        f'<div class="eco-value-sm" style="font-size:0.95rem">{ts_str}</div></div>'
    )
with cb3:
    n_alerts = len(alerts)
    alert_color = GREEN if n_alerts == 0 else ORANGE if n_alerts <= 2 else RED
    health_text = "NOMINAL" if n_alerts == 0 else "ELEVATED" if n_alerts <= 2 else "ATTENTION"
    border = "rgba(0,212,170,0.2)" if n_alerts == 0 else "rgba(255,107,53,0.2)"
    st.html(
        f'<div class="eco-card" style="padding:0.85rem 1rem;min-height:4.8rem;border-color:{border}">'
        f'<div class="eco-label">System Status</div>'
        f'<div class="eco-value-sm" style="color:{alert_color}">{health_text}</div>'
        f'<div style="color:{TEXT_MUTED};font-size:0.72rem;margin-top:0.2rem">'
        f'{n_alerts} active alert{"s" if n_alerts != 1 else ""}</div></div>'
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Hero sustainability score + efficiency sub-gauges ───────────────
g1, g2 = st.columns([1.15, 1.85])
with g1:
    show(sustainability_gauge(score), key="hero_gauge")

with g2:
    e1, e2, e3, e4 = st.columns(4)
    pue_val = mean_vals.get("pue", 0)
    pue_eff = max(0, min(100, (2.0 - pue_val) / 0.8 * 100))
    wue_val = mean_vals.get("wue_l_per_kwh", 0)
    wue_eff = max(0, min(100, (2.5 - wue_val) / 2 * 100))
    cue_val = mean_vals.get("cue_kg_per_kwh", 0)
    cue_eff = max(0, min(100, (0.6 - cue_val) / 0.5 * 100))
    cool_val = mean_vals.get("cooling_efficiency", 0)
    cool_eff = max(0, min(100, cool_val / 5 * 100))

    with e1:
        show(efficiency_mini_gauge(pue_eff, "Energy"), key="eff_energy")
    with e2:
        show(efficiency_mini_gauge(wue_eff, "Water"), key="eff_water")
    with e3:
        show(efficiency_mini_gauge(cue_eff, "Carbon"), key="eff_carbon")
    with e4:
        show(efficiency_mini_gauge(cool_eff, "Cooling"), key="eff_cool")

    # PUE / WUE / CUE compact strip
    p1, p2, p3, p4 = st.columns(4)
    pst, psc = pue_status(pue_val)
    with p1:
        kpi_card_compact("PUE", f"{pue_val:.2f}", pst, psc)
    with p2:
        kpi_card_compact("WUE", f"{wue_val:.2f} L/kWh", "Water Efficiency")
    with p3:
        kpi_card_compact("CUE", f"{cue_val:.3f} kg/kWh", "Carbon Efficiency")
    with p4:
        util = mean_vals.get("server_utilisation_pct", 0)
        kpi_card_compact("Utilisation", f"{util:.1f}%", "Server Load")

# ── Primary KPI strip with sparklines ───────────────────────────────
section_header("Key Performance Indicators", "Period summary with trend indicators")

recent = data.sort_values("timestamp")
k1, k2, k3, k4 = st.columns(4)

def _spark(col, color=GREEN):
    vals = recent[col].tail(72).tolist()
    return sparkline_svg(vals, color=color, width=90, height=22)

with k1:
    total_e = data.total_energy_kwh.sum()
    kpi_card(
        "Facility Energy",
        f"{total_e/1000:,.1f} MWh",
        sparkline_svg=_spark("total_energy_kwh"),
        status="Active",
    )
with k2:
    total_w = data.water_consumption_l.sum()
    kpi_card(
        "Water Consumption",
        f"{total_w/1000:,.1f} kL",
        sparkline_svg=_spark("water_consumption_l", CYAN),
        status="Normal",
    )
with k3:
    total_c = data.carbon_emissions_kg.sum()
    kpi_card(
        "Carbon Emissions",
        f"{total_c/1000:,.1f} tCO₂e",
        sparkline_svg=_spark("carbon_emissions_kg", YELLOW),
        status="Monitoring",
    )
with k4:
    anom_count = int(data.get("anomaly_ground_truth", pd.Series(0)).sum()) if "anomaly_ground_truth" in data.columns else 0
    anom_color = GREEN if anom_count == 0 else ORANGE if anom_count < 10 else RED
    kpi_card(
        "Anomalies Detected",
        str(anom_count),
        status="Clear" if anom_count == 0 else "Review",
    )

# ── AI operations brief ────────────────────────────────────────────
section_header("AI Operations Brief", "Automated insights from current telemetry", icon="🤖")
insights = generate_operations_brief(data)
for ins in insights[:6]:
    insight_card(ins["text"], ins.get("level", "info"))

# ── Live operations timeline ────────────────────────────────────────
section_header("Operations Timeline", "Facility energy, cooling, and anomaly overlay")

anom_markers = data[data.get("anomaly_ground_truth", pd.Series(0, index=data.index)).astype(bool)] if "anomaly_ground_truth" in data.columns else pd.DataFrame()

fig = trend_line(
    recent,
    x="timestamp",
    y=["total_energy_kwh", "cooling_demand_kw", "water_consumption_l"],
    title="Multi-metric Operations Timeline",
    height=380,
    markers=anom_markers if not anom_markers.empty else None,
    marker_col="total_energy_kwh",
)
show(fig, key="ops_timeline")

# ── Digital twin panel + site status ────────────────────────────────
dt_col, site_col = st.columns([3, 2])

with dt_col:
    section_header("Digital Twin — Resource Flow", "Simplified data-centre energy cascade")
    it_load = mean_vals.get("it_load_kw", mean_vals.get("it_energy_kwh", 0))
    it_energy = mean_vals.get("it_energy_kwh", 0)
    cooling = mean_vals.get("cooling_demand_kw", 0)
    total_energy = mean_vals.get("total_energy_kwh", 0)
    carbon = mean_vals.get("carbon_emissions_kg", 0)
    water = mean_vals.get("water_consumption_l", 0)
    util = mean_vals.get("server_utilisation_pct", 0)

    st.html(
        f'<div style="display:grid;grid-template-columns:1fr;gap:0.25rem;max-width:420px;margin:0 auto;width:100%">'
        f'<div class="eco-twin-node"><h4>IT Workload</h4><div class="eco-twin-val">{util:.0f}%</div></div>'
        f'<div class="eco-twin-arrow">▼</div>'
        f'<div class="eco-twin-node"><h4>IT Energy</h4><div class="eco-twin-val">{it_energy:.0f} kWh</div></div>'
        f'<div class="eco-twin-arrow">▼</div>'
        f'<div class="eco-twin-node"><h4>Cooling System</h4><div class="eco-twin-val">{cooling:.0f} kW</div></div>'
        f'<div class="eco-twin-arrow" style="display:flex;justify-content:center;gap:2.5rem">'
        f'<div>▼<br><span style="font-size:0.7rem;color:{CYAN}">Water {water:.0f} L</span></div>'
        f'<div>▼<br><span style="font-size:0.7rem;color:{ORANGE}">Energy</span></div></div>'
        f'<div class="eco-twin-node"><h4>Facility Footprint</h4>'
        f'<div style="display:flex;justify-content:center;gap:1.4rem;flex-wrap:wrap">'
        f'<div><span style="color:{TEXT_MUTED};font-size:0.65rem">Energy</span><br>'
        f'<span class="eco-twin-val" style="font-size:1rem">{total_energy:.0f} kWh</span></div>'
        f'<div><span style="color:{TEXT_MUTED};font-size:0.65rem">Carbon</span><br>'
        f'<span class="eco-twin-val" style="font-size:1rem">{carbon:.1f} kg</span></div>'
        f'</div></div></div>'
    )

with site_col:
    section_header("Multi-Site Status", "Data centre operational overview")
    for s in sites:
        site_data = data[data.site == s]
        s_mean = site_data.mean(numeric_only=True)
        s_pue = s_mean.get("pue", 0)
        s_carbon = "Low" if s_mean.get("cue_kg_per_kwh", 0) < 0.3 else "Moderate" if s_mean.get("cue_kg_per_kwh", 0) < 0.5 else "High"
        s_anom = int(site_data.get("anomaly_ground_truth", pd.Series(0)).sum()) if "anomaly_ground_truth" in site_data.columns else 0
        s_health = max(0, min(100, int(100 - s_anom * 0.5 - max(0, (s_pue - 1.2)) * 30)))
        site_card(s, s_health, s_pue, s_carbon, s_anom, selected=(len(sites) == 1))

# ── Alert centre ────────────────────────────────────────────────────
if alerts:
    section_header("Active Alerts", f"{len(alerts)} alert{'s' if len(alerts) != 1 else ''} requiring attention")
    for a in alerts:
        sev = "HIGH" if any(w in a.lower() for w in ("exceed", "anomaly", "high")) else "MEDIUM"
        alert_strip(sev, a)
else:
    st.html(
        f'<div class="eco-card" style="text-align:center;padding:1rem">'
        f'<span style="color:{GREEN};font-weight:600">✓ No active alerts</span>'
        f'<span style="color:{TEXT_MUTED};font-size:0.82rem"> — All monitored parameters within normal range</span>'
        f'</div>'
    )

# ── Footer ──────────────────────────────────────────────────────────
st.markdown("---")
st.html(
    f'<div style="text-align:center;color:{TEXT_MUTED};font-size:0.72rem;padding:0.5rem 0;line-height:1.55">'
    f'{PRODUCT_NAME} v1.0.0 · AI-Based Sustainability Monitoring System for Data Centres · MSc Dissertation Project<br>'
    f'All values derive from synthetic operational records. Recommendations require qualified engineering review.'
    f'</div>'
)
