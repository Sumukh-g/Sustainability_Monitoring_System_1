"""Executive landing page for the Sustainability Intelligence Centre."""

import streamlit as st
from components.common import filtered_data, get_config, hero, trend
from src.sustainability_metrics import sustainability_score
from src.alerts import active_alerts

st.set_page_config(
    page_title="Sustainability Intelligence Centre", page_icon="🌿", layout="wide"
)
hero(
    "Sustainability Intelligence Centre",
    "Evidence-led operational monitoring and AI decision support for data centres",
)
data, _ = filtered_data()
settings, thresholds = get_config()
if data.empty:
    st.stop()
score, label = sustainability_score(data, settings["sustainability_score_weights"])
cols = st.columns(4)
cols[0].metric("⚡ Energy", f"{data.total_energy_kwh.sum()/1000:,.1f} MWh")
cols[1].metric("💧 Water", f"{data.water_consumption_l.sum()/1000:,.1f} kL")
cols[2].metric("🌱 Carbon", f"{data.carbon_emissions_kg.sum()/1000:,.1f} tCO₂e")
cols[3].metric(
    "Sustainability score",
    f"{score:.0f}/100",
    label,
    help="Project-specific indicator; not an industry standard.",
)
cols = st.columns(4)
cols[0].metric("PUE", f"{data.pue.mean():.2f}")
cols[1].metric("WUE", f"{data.wue_l_per_kwh.mean():.2f} L/kWh")
cols[2].metric("CUE", f"{data.cue_kg_per_kwh.mean():.3f} kg/kWh")
cols[3].metric("Server utilisation", f"{data.server_utilisation_pct.mean():.1f}%")
alerts = active_alerts(data, thresholds)
if alerts:
    st.subheader("Active alerts")
    [st.warning(item) for item in alerts]
trend(
    data, ["total_energy_kwh", "it_energy_kwh", "cooling_energy_kwh"], "Energy profile"
)
st.caption(
    "All values derive from the selected synthetic operational records. Recommendations require qualified engineering review before real-world use."
)
