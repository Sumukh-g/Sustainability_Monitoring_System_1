import streamlit as st
import plotly.express as px
from components.common import filtered_data, get_config, hero
from src.anomaly_detection import detect_anomalies

st.set_page_config(page_title="Anomalies", page_icon="🚨", layout="wide")
hero(
    "AI anomaly detection",
    "Isolation Forest flags multivariate deviations for engineering review",
)
d, _ = filtered_data()
settings, _ = get_config()
if d.empty:
    st.stop()
with st.spinner("Scoring selected observations..."):
    enriched, events, _, metrics = detect_anomalies(
        d, settings["anomaly_contamination"]
    )
sev = st.multiselect(
    "Severity",
    ["Low", "Medium", "High", "Critical"],
    default=["Medium", "High", "Critical"],
)
shown = events[events.severity.astype(str).isin(sev)]
c = st.columns(4)
c[0].metric("Detected", len(events))
c[1].metric("Precision", f"{metrics.get('precision',0):.2f}")
c[2].metric("Recall", f"{metrics.get('recall',0):.2f}")
c[3].metric("F1", f"{metrics.get('f1',0):.2f}")
fig = px.line(
    enriched,
    x="timestamp",
    y="total_energy_kwh",
    color="site",
    title="Energy anomaly timeline",
)
fig.add_scatter(
    x=shown.timestamp,
    y=shown.total_energy_kwh,
    mode="markers",
    name="Anomaly",
    marker=dict(color="#d62728", size=9),
)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(
    shown[
        [
            "timestamp",
            "site",
            "affected_metric",
            "observed_value",
            "expected_range",
            "anomaly_score",
            "severity",
            "probable_explanation",
            "suggested_action",
        ]
    ],
    use_container_width=True,
)
st.caption(
    "Synthetic injected labels enable evaluation but simplify real operational ambiguity; a detected event is not proof of a fault."
)
