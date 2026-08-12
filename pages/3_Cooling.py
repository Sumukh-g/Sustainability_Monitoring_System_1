import streamlit as st
import plotly.express as px
from components.common import filtered_data, hero

st.set_page_config(page_title="Cooling", page_icon="❄️", layout="wide")
hero("Cooling analytics", "Demand, energy, efficiency and likely operating drivers")
d, _ = filtered_data()
if d.empty:
    st.stop()
cooling_figure = px.line(
    d,
    x="timestamp",
    y=["cooling_demand_kw", "cooling_energy_kwh"],
    title="Cooling demand and energy",
)
cooling_events = d[(d.anomaly_ground_truth == 1) & (d.anomaly_type == "Cooling fault")]
cooling_figure.add_scatter(
    x=cooling_events.timestamp,
    y=cooling_events.cooling_demand_kw,
    mode="markers",
    name="Injected cooling event",
    marker={"color": "#d62728", "size": 9},
)
st.plotly_chart(cooling_figure, use_container_width=True)
c1, c2 = st.columns(2)
c1.plotly_chart(
    px.scatter(
        d,
        x="external_temperature_c",
        y="cooling_demand_kw",
        color="cooling_efficiency",
        title="Cooling vs outdoor temperature",
    ),
    use_container_width=True,
)
c2.plotly_chart(
    px.scatter(
        d,
        x="it_load_kw",
        y="cooling_demand_kw",
        color="site",
        title="Cooling vs IT load",
    ),
    use_container_width=True,
)
