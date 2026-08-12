import streamlit as st
import plotly.express as px
from components.common import filtered_data, hero

st.set_page_config(page_title="Carbon", page_icon="🌱", layout="wide")
hero(
    "Carbon analytics", "Location-based emissions, grid intensity and renewable context"
)
d, _ = filtered_data()
if d.empty:
    st.stop()
st.plotly_chart(
    px.line(
        d,
        x="timestamp",
        y=["carbon_emissions_kg", "grid_carbon_intensity_g_per_kwh"],
        title="Emissions and grid intensity",
    ),
    use_container_width=True,
)
c1, c2 = st.columns(2)
c1.plotly_chart(
    px.scatter(
        d,
        x="total_energy_kwh",
        y="carbon_emissions_kg",
        color="renewable_energy_pct",
        title="Carbon vs energy",
    ),
    use_container_width=True,
)
c2.plotly_chart(
    px.line(d, x="timestamp", y="cue_kg_per_kwh", color="site", title="CUE"),
    use_container_width=True,
)
