import streamlit as st
import plotly.express as px
from components.common import filtered_data, hero
from src.data_loader import validate_data

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")
hero("Data explorer", "Schema, quality, descriptive statistics and export")
d, _ = filtered_data()
tabs = st.tabs(["Records", "Quality", "Statistics", "Correlation"])
with tabs[0]:
    st.dataframe(d, use_container_width=True)
    st.download_button(
        "Download filtered CSV", d.to_csv(index=False), "filtered_data.csv", "text/csv"
    )
with tabs[1]:
    st.dataframe(validate_data(d), use_container_width=True)
    st.dataframe(d.isna().sum().rename("missing"))
with tabs[2]:
    st.dataframe(
        (
            d.describe(include="all", datetime_is_numeric=True)
            if False
            else d.describe(include="all")
        ),
        use_container_width=True,
    )
with tabs[3]:
    numeric = d.select_dtypes("number")
    st.plotly_chart(
        px.imshow(
            numeric.corr(),
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            title="Correlation (association, not causality)",
        ),
        use_container_width=True,
    )
