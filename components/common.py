"""Shared dashboard data, controls, and visual styling."""

from pathlib import Path
import pandas as pd
import streamlit as st
import yaml
from src.data_loader import load_data

st.markdown(
    """<style>.stApp{background:#f5f8f6}.block-container{padding-top:2rem}.hero{padding:1.3rem;border-radius:14px;background:linear-gradient(120deg,#073b32,#147d64);color:white;margin-bottom:1rem}[data-testid=stMetric]{background:white;border:1px solid #dce8e2;padding:14px;border-radius:12px}</style>""",
    unsafe_allow_html=True,
)


@st.cache_data
def get_data(path="data/generated/data_centre_hourly.csv"):
    return load_data(path)


@st.cache_data
def get_config():
    return yaml.safe_load(Path("config/settings.yaml").read_text()), yaml.safe_load(
        Path("config/thresholds.yaml").read_text()
    )


def filtered_data():
    data = get_data()
    st.sidebar.header("Global controls")
    sites = st.sidebar.multiselect(
        "Site", sorted(data.site.unique()), default=sorted(data.site.unique())
    )
    minimum, maximum = data.timestamp.min().date(), data.timestamp.max().date()
    dates = st.sidebar.date_input(
        "Date range",
        (max(minimum, maximum - pd.Timedelta(days=30)), maximum),
        min_value=minimum,
        max_value=maximum,
    )
    aggregation = st.sidebar.selectbox(
        "Aggregation", ["Hourly", "Daily", "Weekly", "Monthly"], index=1
    )
    if st.sidebar.button("Refresh data"):
        st.cache_data.clear()
        st.rerun()
    if len(dates) != 2:
        st.warning("Choose a start and end date.")
        return data.iloc[0:0], aggregation
    start, end = pd.Timestamp(dates[0]), pd.Timestamp(dates[1]) + pd.Timedelta(days=1)
    selected = data[
        data.site.isin(sites) & data.timestamp.between(start, end, inclusive="left")
    ]
    if selected.empty:
        st.error("No observations match these filters.")
    return selected, aggregation


def hero(title, subtitle):
    st.markdown(
        f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def trend(data, columns, title):
    import plotly.express as px

    long = data.melt(
        id_vars="timestamp", value_vars=columns, var_name="Metric", value_name="Value"
    )
    st.plotly_chart(
        px.line(
            long,
            x="timestamp",
            y="Value",
            color="Metric",
            title=title,
            template="plotly_white",
        ),
        use_container_width=True,
    )
