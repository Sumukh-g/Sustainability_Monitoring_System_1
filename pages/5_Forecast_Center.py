"""EcoNexus AI — AI Forecast Center."""

from __future__ import annotations

from pathlib import Path
import json

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.layout import page_chrome, global_filters, get_config, empty_state
from ui.cards import kpi_card_compact, section_header, stat_row
from ui.charts import show
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, BLUE, ORANGE, RED, YELLOW,
    CHART_COLORS,
)
from src.forecasting import predict_test
from src.explainability import feature_importance

# ── Page shell ───────────────────────────────────────────────────────
page_chrome(
    "AI Forecast Center",
    "Machine learning predictions with model confidence metrics",
    "🔮",
)
data, agg = global_filters()
if data.empty:
    st.stop()

settings, thresholds = get_config()

# ── Controls ─────────────────────────────────────────────────────────
ctrl1, ctrl2 = st.columns([1, 2])
with ctrl1:
    target = st.selectbox(
        "Forecast Target",
        ["total_energy_kwh", "cooling_demand_kw", "water_consumption_l"],
        format_func=lambda x: x.replace("_", " ").title(),
        key="fc_target",
    )
with ctrl2:
    horizon = st.slider(
        "Display Horizon (hours)", 24, 336, 168, key="fc_horizon"
    )

target_label = target.replace("_", " ").title()

try:
    pred = predict_test(data, target).tail(horizon)

    # ── Section: Current Forecast ────────────────────────────────────
    section_header(
        "Current Forecast",
        "Actual vs model prediction on held-out data",
        "📈",
    )

    fig_forecast = go.Figure()
    fig_forecast.add_trace(
        go.Scatter(
            x=pred["timestamp"],
            y=pred[target],
            name="Actual",
            line=dict(color=GREEN, width=2),
            mode="lines",
        )
    )
    fig_forecast.add_trace(
        go.Scatter(
            x=pred["timestamp"],
            y=pred["predicted"],
            name="Predicted",
            line=dict(color=CYAN, width=2, dash="dot"),
            mode="lines",
        )
    )
    fig_forecast.update_layout(
        title=f"{target_label} — Actual vs Predicted",
        height=400,
        xaxis_title="Time",
        yaxis_title=target_label,
    )
    show(fig_forecast, key="fc_overlay")

    # ── Section: Model Confidence ────────────────────────────────────
    section_header(
        "Model Confidence",
        "Production model performance metrics",
        "🎯",
    )

    meta_path = Path(f"models/metadata/{target}.json")
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            kpi_card_compact("Model", meta["model_name"], color=GREEN)
        with mc2:
            kpi_card_compact("RMSE", f"{meta['rmse']:.4f}", color=CYAN)
        with mc3:
            kpi_card_compact("MAE", f"{meta['mae']:.4f}", color=BLUE)
        with mc4:
            r2_val = meta["r2"]
            r2_color = GREEN if r2_val > 0.9 else YELLOW if r2_val > 0.7 else RED
            kpi_card_compact("R²", f"{r2_val:.4f}", color=r2_color)

        stat_row([
            ("Training Samples", f"{meta.get('training_samples', '—'):,}", ""),
            ("Test Samples", f"{meta.get('test_samples', '—'):,}", ""),
            ("Train Period", str(meta.get("training_start", "—"))[:10], ""),
            ("Test Period", str(meta.get("test_start", "—"))[:10], ""),
        ])
    else:
        empty_state("📄", "No metadata", f"Metadata file not found for {target_label}")

    # ── Section: Model Leaderboard ───────────────────────────────────
    comparison_path = Path("reports/evaluation/model_comparison.csv")
    if comparison_path.exists():
        all_comp = pd.read_csv(comparison_path)
        target_comp = (
            all_comp[all_comp["Target"] == target]
            if "Target" in all_comp.columns
            else all_comp
        ).copy()

        if not target_comp.empty:
            section_header(
                "Model Leaderboard",
                f"All evaluated models for {target_label}",
                "🏆",
            )

            selected_model = (
                meta["model_name"] if meta_path.exists() else None
            )
            if selected_model and "Model" in target_comp.columns:
                target_comp["Selected"] = target_comp["Model"].eq(selected_model)
                target_comp = target_comp.sort_values("RMSE")
            st.dataframe(target_comp, width="stretch")

    # ── Section: Feature Intelligence ────────────────────────────────
    section_header(
        "Feature Intelligence — What Drives the Forecast?",
        "Model feature associations (not causal effects)",
        "🧠",
    )

    model_path = Path(f"models/forecasting/{target}.joblib")
    if model_path.exists():
        try:
            artifact = joblib.load(model_path)
            fi = feature_importance(artifact).head(15)

            fig_fi = go.Figure(
                go.Bar(
                    x=fi["importance"],
                    y=fi["feature"].apply(
                        lambda f: f.replace("_", " ").title()
                    ),
                    orientation="h",
                    marker_color=[
                        CHART_COLORS[i % len(CHART_COLORS)]
                        for i in range(len(fi))
                    ],
                )
            )
            fig_fi.update_layout(
                title="Top 15 Feature Importance",
                height=450,
                yaxis=dict(autorange="reversed"),
                xaxis_title="Importance",
            )
            show(fig_fi, key="fc_feat_imp")
        except Exception:
            empty_state(
                "🧠",
                "Feature analysis unavailable",
                "Could not load model for feature inspection",
            )
    else:
        empty_state(
            "🧠",
            "Model not found",
            "No trained model found — run the training pipeline first",
        )

    # ── Section: Residual Analysis ───────────────────────────────────
    section_header(
        "Residual Analysis",
        "Distribution of prediction errors",
        "📊",
    )

    fig_resid = go.Figure(
        go.Histogram(
            x=pred["residual"],
            nbinsx=40,
            marker_color=GREEN,
            marker_line_color=BORDER,
            marker_line_width=1,
            opacity=0.8,
        )
    )
    fig_resid.update_layout(
        title="Residual Distribution (Actual − Predicted)",
        height=350,
        xaxis_title="Residual",
        yaxis_title="Count",
    )
    show(fig_resid, key="fc_resid_hist")

    stat_row([
        ("Mean Residual", f"{pred['residual'].mean():.4f}", ""),
        ("Std Deviation", f"{pred['residual'].std():.4f}", ""),
        ("Min Error", f"{pred['residual'].min():.2f}", ""),
        ("Max Error", f"{pred['residual'].max():.2f}", ""),
    ])

except FileNotFoundError as exc:
    empty_state("🔮", "Forecast model not available", str(exc))
except Exception as exc:
    empty_state("⚠️", "Forecast error", str(exc))
