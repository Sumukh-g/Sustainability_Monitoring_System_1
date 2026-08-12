import streamlit as st
import plotly.express as px
from components.common import filtered_data, hero

st.set_page_config(page_title="Water", page_icon="💧", layout="wide")
hero("Water analytics", "Water trends, intensity and cooling relationships")
d, _ = filtered_data()
if d.empty:
    st.stop()
c1, c2 = st.columns(2)
water_figure = px.line(
    d,
    x="timestamp",
    y=["water_consumption_l", "cooling_water_l"],
    title="Water consumption",
)
water_events = d[(d.anomaly_ground_truth == 1) & (d.anomaly_type == "Water leak")]
water_figure.add_scatter(
    x=water_events.timestamp,
    y=water_events.water_consumption_l,
    mode="markers",
    name="Injected water event",
    marker={"color": "#d62728", "size": 9},
)
c1.plotly_chart(water_figure, use_container_width=True)
c2.plotly_chart(
    px.scatter(
        d,
        x="cooling_demand_kw",
        y="water_consumption_l",
        color="external_temperature_c",
        title="Water vs cooling demand",
    ),
    use_container_width=True,
)
st.plotly_chart(
    px.line(d, x="timestamp", y="wue_l_per_kwh", color="site", title="WUE (L/kWh IT)"),
    use_container_width=True,
)
