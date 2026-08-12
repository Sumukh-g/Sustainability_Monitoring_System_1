import streamlit as st
import plotly.express as px
from components.common import filtered_data, hero
from src.forecasting import predict_test

st.set_page_config(page_title="AI Forecasting", page_icon="📈", layout="wide")
hero("AI forecasting", "Chronological held-out predictions and residual inspection")
d, _ = filtered_data()
target = st.selectbox(
    "Target", ["total_energy_kwh", "cooling_demand_kw", "water_consumption_l"]
)
horizon = st.slider("Display horizon (hours)", 24, 336, 168)
try:
    pred = predict_test(d, target).tail(horizon)
    long = (
        pred[["timestamp", target, "predicted"]]
        .rename(columns={target: "observed"})
        .melt("timestamp", var_name="Series", value_name="Value")
    )
    st.plotly_chart(
        px.line(
            long,
            x="timestamp",
            y="Value",
            color="Series",
            title="Observed vs persisted-model prediction",
        ),
        use_container_width=True,
    )
    st.plotly_chart(
        px.bar(pred, x="timestamp", y="residual", title="Residuals"),
        use_container_width=True,
    )
    st.info(
        "The displayed horizon is a held-out backtest. Approximate uncertainty is visible through residual variation; it is not a formal confidence interval."
    )
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
