import streamlit as st
from components.common import filtered_data, hero

st.set_page_config(page_title="What-if", page_icon="🧪", layout="wide")
hero(
    "What-if simulator · Advanced",
    "Modelled estimates for exploration—not observed outcomes or control instructions",
)
d, _ = filtered_data()
if d.empty:
    st.stop()
base = d.tail(min(168, len(d))).mean(numeric_only=True)
load = st.slider("IT load change (%)", -30, 30, 0)
temp = st.slider("External temperature change (°C)", -5, 8, 0)
efficiency = st.slider("Cooling efficiency change (%)", -25, 25, 0)
renewable = st.slider("Renewable proportion change (percentage points)", -20, 30, 0)
it = base.it_energy_kwh * (1 + load / 100)
cooling = (
    base.cooling_demand_kw
    * (1 + load / 200 + max(temp, 0) * 0.025)
    / (base.cooling_efficiency * (1 + efficiency / 100))
)
total = (
    it
    + cooling
    + (base.total_energy_kwh - base.it_energy_kwh - base.cooling_energy_kwh)
)
water = base.water_consumption_l * (1 + load / 250 + max(temp, 0) * 0.035)
carbon = total * base.grid_carbon_intensity_g_per_kwh / 1000 * (1 - renewable / 200)
c = st.columns(4)
c[0].metric(
    "Estimated energy",
    f"{total:.1f} kWh",
    f"{(total/base.total_energy_kwh-1)*100:.1f}%",
)
c[1].metric(
    "Estimated water",
    f"{water:.1f} L",
    f"{(water/base.water_consumption_l-1)*100:.1f}%",
)
c[2].metric(
    "Estimated carbon",
    f"{carbon:.1f} kg",
    f"{(carbon/base.carbon_emissions_kg-1)*100:.1f}%",
)
c[3].metric("Estimated PUE", f"{total/it:.2f}")
st.caption(
    "Estimates use transparent engineering sensitivities calibrated to recent means. They are not causal forecasts and require facilities-engineering validation."
)
