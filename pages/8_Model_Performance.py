from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
from components.common import hero
from src.explainability import feature_importance

st.set_page_config(page_title="Model Performance", page_icon="📊", layout="wide")
hero(
    "Model performance",
    "Genuine held-out metrics, baseline comparison, residuals and associations",
)
comparison = Path("reports/evaluation/model_comparison.csv")
if not comparison.exists():
    st.error("Evaluation output missing. Run python -m src.forecasting")
    st.stop()
table = pd.read_csv(comparison)
st.dataframe(table, use_container_width=True)
st.plotly_chart(
    px.bar(
        table,
        x="Model",
        y="RMSE",
        color="Model",
        title="Held-out RMSE (lower is better)",
    ),
    use_container_width=True,
)
pred_path = Path("reports/evaluation/test_predictions.csv")
if pred_path.exists():
    p = pd.read_csv(pred_path)
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.scatter(
            p, x="actual", y="predicted", title="Actual vs predicted", opacity=0.35
        ),
        use_container_width=True,
    )
    c2.plotly_chart(
        px.histogram(p, x="residual", title="Residual distribution"),
        use_container_width=True,
    )
metadata = Path("models/metadata/total_energy_kwh.json")
if metadata.exists():
    meta = json.loads(metadata.read_text())
    st.subheader(f"Selected production model: {meta['model_name']}")
    st.json(meta)
    artifact = joblib.load("models/forecasting/total_energy_kwh.joblib")
    st.plotly_chart(
        px.bar(
            feature_importance(artifact).head(15),
            x="importance",
            y="feature",
            orientation="h",
            title="Model feature associations (not causal effects)",
        ),
        use_container_width=True,
    )
