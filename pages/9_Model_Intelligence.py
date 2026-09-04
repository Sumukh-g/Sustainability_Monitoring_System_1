"""EcoNexus AI — Model Intelligence Center."""

from __future__ import annotations
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ui.layout import page_chrome, get_data, empty_state
from ui.cards import section_header, kpi_card_compact, stat_row
from ui.charts import bar_chart, scatter, show
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, BLUE, ORANGE, RED, YELLOW, CHART_COLORS,
)

TARGETS = ["total_energy_kwh", "cooling_demand_kw", "water_consumption_l"]


page_chrome(
    "Model Intelligence",
    "Production model evaluation, diagnostics, and explainability",
    "🧠",
)

# ── Section: Production Models ───────────────────────────────────────────────

section_header("Production Models", "Deployed model summary across all targets", "📦")

meta_cols = st.columns(len(TARGETS))
for idx, target in enumerate(TARGETS):
    meta_path = Path(f"models/metadata/{target}.json")
    with meta_cols[idx]:
        try:
            if not meta_path.exists():
                raise FileNotFoundError
            meta = json.loads(meta_path.read_text())
            kpi_card_compact(
                target.replace("_", " ").title(),
                meta.get("model_name", "Unknown"),
                sub=f"R² {meta.get('r2', 0):.3f} · RMSE {meta.get('rmse', 0):.2f}",
                color=GREEN,
            )
        except Exception:
            kpi_card_compact(target.replace("_", " ").title(), "Not available", color=TEXT_MUTED)

# ── Section: Model Leaderboard ───────────────────────────────────────────────

section_header("Model Leaderboard", "Comparative performance across algorithms", "🏆")

comparison_path = Path("reports/evaluation/model_comparison.csv")
try:
    if not comparison_path.exists():
        raise FileNotFoundError
    comparison_df = pd.read_csv(comparison_path)

    targets_available = sorted(comparison_df["Target"].unique()) if "Target" in comparison_df.columns else TARGETS
    lb_target = st.selectbox("Filter by target", targets_available, key="lb_target")

    filtered_comp = comparison_df[comparison_df["Target"] == lb_target] if "Target" in comparison_df.columns else comparison_df

    st.dataframe(
        filtered_comp.style.highlight_min(subset=["RMSE"], color="rgba(0,212,170,0.15)")
        if "RMSE" in filtered_comp.columns else filtered_comp,
        width="stretch",
    )

    if "RMSE" in filtered_comp.columns and "Model" in filtered_comp.columns:
        fig = bar_chart(filtered_comp, x="Model", y="RMSE", title="RMSE Comparison (lower is better)")
        show(fig, key="leaderboard_rmse")

except Exception:
    empty_state("📊", "Leaderboard unavailable", "Run the evaluation pipeline to generate model_comparison.csv")

# ── Section: Generalisation Performance ──────────────────────────────────────

section_header("Generalisation Performance", "Held-out test set predictions and residual analysis", "🎯")

gp_target = st.selectbox("Select target", TARGETS, key="gp_target")
pred_path = Path(f"reports/evaluation/test_predictions_{gp_target}.csv")

try:
    if not pred_path.exists():
        raise FileNotFoundError
    preds = pd.read_csv(pred_path)

    c1, c2 = st.columns(2)
    with c1:
        fig_scatter = scatter(
            preds, x="actual", y="predicted",
            title=f"Actual vs Predicted — {gp_target.replace('_', ' ').title()}",
        )
        fig_scatter.add_trace(go.Scatter(
            x=[preds["actual"].min(), preds["actual"].max()],
            y=[preds["actual"].min(), preds["actual"].max()],
            mode="lines", name="Perfect",
            line=dict(dash="dash", color=TEXT_MUTED, width=1),
        ))
        show(fig_scatter, key="gp_scatter")

    with c2:
        fig_hist = px.histogram(
            preds, x="residual",
            title=f"Residual Distribution — {gp_target.replace('_', ' ').title()}",
            nbins=50, opacity=0.7,
        )
        fig_hist.update_traces(marker_color=CYAN)
        fig_hist.update_layout(height=340)
        show(fig_hist, key="gp_residuals")

except Exception:
    empty_state("🎯", "Predictions not available", f"No test predictions found for {gp_target}")

# ── Section: Feature Intelligence ────────────────────────────────────────────

section_header("Feature Intelligence", "Model feature associations (not causal effects)", "🔬")

fi_target = st.selectbox("Select target", TARGETS, key="fi_target")
model_path = Path(f"models/forecasting/{fi_target}.joblib")

try:
    if not model_path.exists():
        raise FileNotFoundError
    from src.explainability import feature_importance

    artifact = joblib.load(model_path)
    importance_df = feature_importance(artifact).head(15)

    fig_fi = bar_chart(
        importance_df, x="importance", y="feature",
        title=f"Top Feature Associations — {fi_target.replace('_', ' ').title()}",
        horizontal=True, height=420,
    )
    fig_fi.update_traces(marker_color=GREEN)
    show(fig_fi, key="feature_importance")

    st.html(
        '<div class="eco-insight">These values represent statistical associations learned by the model. '
        'They do not establish causal relationships between features and the target variable.</div>'
    )

except Exception:
    empty_state("🔬", "Feature analysis unavailable", f"Model artifact not found for {fi_target}")

# ── Section: Anomaly Model Performance ───────────────────────────────────────

section_header("Anomaly Model Performance", "Isolation Forest detection quality against ground truth", "🛡️")

try:
    data = get_data()
    if data.empty:
        raise ValueError("No data")

    from src.anomaly_detection import detect_anomalies

    enriched, events, _model, metrics = detect_anomalies(data, contamination=0.025)

    if metrics:
        m_cols = st.columns(4)
        with m_cols[0]:
            kpi_card_compact("Precision", f"{metrics['precision']:.3f}", color=GREEN)
        with m_cols[1]:
            kpi_card_compact("Recall", f"{metrics['recall']:.3f}", color=CYAN)
        with m_cols[2]:
            kpi_card_compact("F1 Score", f"{metrics['f1']:.3f}", color=BLUE)
        with m_cols[3]:
            kpi_card_compact("Detected", str(metrics.get("detected", 0)), color=ORANGE)

        cm = metrics.get("confusion_matrix")
        if cm:
            cm_array = np.array(cm)
            fig_cm = px.imshow(
                cm_array,
                labels=dict(x="Predicted", y="Actual", color="Count"),
                x=["Normal", "Anomaly"],
                y=["Normal", "Anomaly"],
                title="Confusion Matrix",
                color_continuous_scale=[[0, "rgba(17,17,17,1)"], [1, GREEN]],
                text_auto=True,
            )
            fig_cm.update_layout(height=340)
            show(fig_cm, key="anomaly_cm")
    else:
        st.info("Ground truth labels not available for evaluation.")

except Exception as e:
    empty_state("🛡️", "Anomaly evaluation unavailable", str(e))

# ── Section: Training Metadata ───────────────────────────────────────────────

section_header("Training Metadata", "Model versioning and training provenance", "📋")

tm_target = st.selectbox("Select target", TARGETS, key="tm_target")
tm_meta_path = Path(f"models/metadata/{tm_target}.json")

try:
    if not tm_meta_path.exists():
        raise FileNotFoundError
    tm_meta = json.loads(tm_meta_path.read_text())

    stat_row([
        ("Model", tm_meta.get("model_name", "—"), ""),
        ("Training Date", str(tm_meta.get("training_date", "—")), ""),
        ("Training Samples", f"{tm_meta.get('training_samples', 0):,}", "rows"),
        ("Test Samples", f"{tm_meta.get('test_samples', 0):,}", "rows"),
        ("Features", str(tm_meta.get("feature_count", tm_meta.get("n_features", "—"))), "inputs"),
        ("Version", str(tm_meta.get("model_version", "1.0")), ""),
    ])

except Exception:
    empty_state("📋", "Metadata not available", f"No metadata file found for {tm_target}")
