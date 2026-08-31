"""EcoNexus AI — AI Scenario Lab."""

from __future__ import annotations

import numpy as np
import streamlit as st

from ui.layout import page_chrome, global_filters, get_config, empty_state
from ui.cards import kpi_card, kpi_card_compact, section_header, stat_row
from ui.charts import radar_chart, show
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, BLUE, ORANGE, RED, YELLOW,
)
from src.sustainability_metrics import sustainability_score

# ── Page shell ───────────────────────────────────────────────────────
page_chrome(
    "AI Scenario Lab",
    "What-if simulation for sustainability strategy exploration",
    "🧪",
)
data, agg = global_filters()
if data.empty:
    st.stop()

settings, thresholds = get_config()

# ── Base values from recent data ─────────────────────────────────────
base = data.tail(min(168, len(data))).mean(numeric_only=True)

# ── Section: Scenario Configuration ──────────────────────────────────
section_header(
    "Scenario Configuration",
    "Adjust parameters to explore sustainability strategy trade-offs",
    "⚙️",
)

s1, s2 = st.columns(2)
with s1:
    load_change = st.slider(
        "IT Load Change (%)", -30, 30, 0, key="sc_load",
        help="Simulate increasing or decreasing IT workload",
    )
    temp_change = st.slider(
        "External Temperature Change (°C)", -5, 8, 0, key="sc_temp",
        help="Simulate warmer or cooler ambient conditions",
    )
with s2:
    eff_change = st.slider(
        "Cooling Efficiency Change (%)", -25, 25, 0, key="sc_eff",
        help="Simulate improvements or degradation in cooling plant",
    )
    renew_change = st.slider(
        "Renewable Proportion Change (pp)", -20, 30, 0, key="sc_renew",
        help="Simulate increased or decreased renewable energy mix",
    )

# ── Scenario calculations (same engineering sensitivities as original) ─
sc_it = base.it_energy_kwh * (1 + load_change / 100)

cooling_eff = base.cooling_efficiency * (1 + eff_change / 100)
cooling_eff = max(cooling_eff, 0.01)
sc_cooling = (
    base.cooling_demand_kw
    * (1 + load_change / 200 + max(temp_change, 0) * 0.025)
    / cooling_eff
    * base.cooling_efficiency
)

other_energy = base.total_energy_kwh - base.it_energy_kwh - base.cooling_energy_kwh
sc_total = sc_it + sc_cooling + other_energy

sc_water = base.water_consumption_l * (
    1 + load_change / 250 + max(temp_change, 0) * 0.035
)

sc_carbon = (
    sc_total
    * base.grid_carbon_intensity_g_per_kwh
    / 1000
    * (1 - renew_change / 200)
)

sc_pue = sc_total / sc_it if sc_it > 0 else float("nan")

# ── Deltas ───────────────────────────────────────────────────────────
energy_delta = (sc_total / base.total_energy_kwh - 1) * 100 if base.total_energy_kwh else 0
water_delta = (sc_water / base.water_consumption_l - 1) * 100 if base.water_consumption_l else 0
carbon_delta = (sc_carbon / base.carbon_emissions_kg - 1) * 100 if base.carbon_emissions_kg else 0
pue_delta = sc_pue - base.pue if not np.isnan(sc_pue) else 0

# ── Sustainability scores ────────────────────────────────────────────
current_score, current_label = sustainability_score(data)

scenario_data = data.tail(min(168, len(data))).copy()
try:
    scenario_data["total_energy_kwh"] = scenario_data["total_energy_kwh"] * (sc_total / base.total_energy_kwh)
    scenario_data["water_consumption_l"] = scenario_data["water_consumption_l"] * (sc_water / base.water_consumption_l)
    scenario_data["carbon_emissions_kg"] = scenario_data["carbon_emissions_kg"] * (sc_carbon / base.carbon_emissions_kg)
    scenario_score, scenario_label = sustainability_score(scenario_data)
except Exception:
    scenario_score, scenario_label = current_score, current_label

# ── Section: Side-by-Side Comparison ─────────────────────────────────
section_header(
    "Side-by-Side Comparison",
    "Current operational state versus simulated scenario",
    "⚖️",
)


def _delta_color(delta: float, inverted: bool = False) -> str:
    if abs(delta) < 0.5:
        return TEXT_MUTED
    positive_is_good = inverted
    is_positive = delta > 0
    return GREEN if (is_positive == positive_is_good) else RED


def _delta_arrow(delta: float) -> str:
    if abs(delta) < 0.1:
        return "→"
    return "↑" if delta > 0 else "↓"


metrics_comparison = [
    ("Energy (kWh)", f"{base.total_energy_kwh:.1f}", f"{sc_total:.1f}", energy_delta, False),
    ("Water (L)", f"{base.water_consumption_l:.1f}", f"{sc_water:.1f}", water_delta, False),
    ("Carbon (kg)", f"{base.carbon_emissions_kg:.1f}", f"{sc_carbon:.1f}", carbon_delta, False),
    ("PUE", f"{base.pue:.3f}", f"{sc_pue:.3f}", pue_delta * 100, False),
    ("Sustainability", f"{current_score:.0f} ({current_label})", f"{scenario_score:.0f} ({scenario_label})", scenario_score - current_score, True),
]

compare_html = f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1rem">
    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem 1.2rem">
        <div style="font-size:0.72rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.12em;font-weight:700;margin-bottom:0.8rem;text-align:center">
            CURRENT STATE
        </div>
"""

for label, current_val, _, _, _ in metrics_comparison:
    compare_html += f"""
        <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid {BORDER}">
            <span style="font-size:0.85rem;color:{TEXT_SECONDARY}">{label}</span>
            <span style="font-size:0.85rem;font-weight:600;color:{TEXT}">{current_val}</span>
        </div>
    """

compare_html += f"""
    </div>
    <div style="background:{BG_CARD};border:1px solid rgba(0,180,216,0.2);border-radius:12px;padding:1rem 1.2rem">
        <div style="font-size:0.72rem;color:{CYAN};text-transform:uppercase;letter-spacing:0.12em;font-weight:700;margin-bottom:0.8rem;text-align:center">
            SCENARIO
        </div>
"""

for label, _, sc_val, delta, inverted in metrics_comparison:
    d_color = _delta_color(delta, inverted)
    arrow = _delta_arrow(delta)
    compare_html += f"""
        <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid {BORDER}">
            <span style="font-size:0.85rem;color:{TEXT_SECONDARY}">{label}</span>
            <span>
                <span style="font-size:0.85rem;font-weight:600;color:{TEXT}">{sc_val}</span>
                <span style="font-size:0.75rem;color:{d_color};margin-left:0.4rem">{arrow} {delta:+.1f}%</span>
            </span>
        </div>
    """

compare_html += """
    </div>
</div>
"""
st.markdown(compare_html, unsafe_allow_html=True)

# ── Section: Estimated Impact ────────────────────────────────────────
section_header(
    "Estimated Impact",
    "Key sustainability metric changes under the scenario",
    "📊",
)

i1, i2, i3, i4 = st.columns(4)
with i1:
    e_dir = "down" if energy_delta < -0.5 else "up" if energy_delta > 0.5 else "neutral"
    kpi_card(
        "Energy Change",
        f"{energy_delta:+.1f}%",
        delta=f"{sc_total:.0f} kWh",
        delta_direction=e_dir,
        status="optimal" if energy_delta < -2 else "warning" if energy_delta > 2 else "good",
        icon="⚡",
    )
with i2:
    w_dir = "down" if water_delta < -0.5 else "up" if water_delta > 0.5 else "neutral"
    kpi_card(
        "Water Change",
        f"{water_delta:+.1f}%",
        delta=f"{sc_water:.0f} L",
        delta_direction=w_dir,
        status="optimal" if water_delta < -2 else "warning" if water_delta > 2 else "good",
        icon="💧",
    )
with i3:
    c_dir = "down" if carbon_delta < -0.5 else "up" if carbon_delta > 0.5 else "neutral"
    kpi_card(
        "Carbon Change",
        f"{carbon_delta:+.1f}%",
        delta=f"{sc_carbon:.0f} kg",
        delta_direction=c_dir,
        status="optimal" if carbon_delta < -2 else "warning" if carbon_delta > 2 else "good",
        icon="🌍",
    )
with i4:
    pue_dir = "down" if pue_delta < -0.01 else "up" if pue_delta > 0.01 else "neutral"
    kpi_card(
        "PUE Change",
        f"{sc_pue:.3f}",
        delta=f"{pue_delta:+.3f} vs {base.pue:.3f}",
        delta_direction=pue_dir,
        status="optimal" if sc_pue < 1.3 else "warning" if sc_pue < 1.6 else "critical",
        icon="📈",
    )

# ── Section: Multi-Dimensional Comparison ────────────────────────────
section_header(
    "Multi-Dimensional Comparison",
    "Radar view across sustainability dimensions",
    "🕸️",
)

def _score_dim(value: float, best: float, worst: float) -> float:
    if best == worst:
        return 50.0
    raw = (value - worst) / (best - worst) * 100
    return float(np.clip(raw, 0, 100))

categories = [
    "Energy Efficiency",
    "Water Efficiency",
    "Carbon Efficiency",
    "Cooling Efficiency",
    "Utilisation",
]

current_vals = [
    _score_dim(base.pue, 1.0, 2.5),
    _score_dim(base.wue_l_per_kwh, 0.0, 3.0),
    _score_dim(base.cue_kg_per_kwh, 0.0, 0.8),
    _score_dim(base.cooling_efficiency, 5.0, 0.0),
    _score_dim(base.server_utilisation_pct, 100.0, 0.0),
]

sc_wue = sc_water / sc_it if sc_it > 0 else base.wue_l_per_kwh
sc_cue = sc_carbon / sc_it if sc_it > 0 else base.cue_kg_per_kwh

scenario_vals = [
    _score_dim(sc_pue, 1.0, 2.5),
    _score_dim(sc_wue, 0.0, 3.0),
    _score_dim(sc_cue, 0.0, 0.8),
    _score_dim(cooling_eff, 5.0, 0.0),
    _score_dim(base.server_utilisation_pct * (1 + load_change / 100), 100.0, 0.0),
]

fig_radar = radar_chart(
    categories,
    current_vals,
    scenario_vals,
    title="Current vs Scenario — Sustainability Dimensions",
    height=420,
)
show(fig_radar, key="sc_radar")

# ── Disclaimer ───────────────────────────────────────────────────────
st.caption(
    "Scenario model — estimates based on engineering sensitivities, not measured "
    "operational savings. Results require facilities-engineering validation before "
    "any operational decisions."
)
