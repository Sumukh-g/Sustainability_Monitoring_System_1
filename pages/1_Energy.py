import streamlit as st
import plotly.express as px
from components.common import filtered_data, hero, trend

st.set_page_config(page_title="Energy", page_icon="⚡", layout="wide")
hero("Energy analytics", "Facility, IT, cooling, peaks and workload relationships")
d, _ = filtered_data()
if d.empty:
    st.stop()
trend(
    d,
    ["total_energy_kwh", "it_energy_kwh", "cooling_energy_kwh"],
    "Hourly energy components",
)
c1, c2 = st.columns(2)
c1.plotly_chart(
    px.scatter(
        d,
        x="compute_workload_units",
        y="total_energy_kwh",
        color="external_temperature_c",
        title="Energy vs workload",
    ),
    use_container_width=True,
)
c2.plotly_chart(
    px.line(d, x="timestamp", y="pue", color="site", title="PUE over time"),
    use_container_width=True,
)
