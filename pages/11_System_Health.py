"""EcoNexus AI — System Health Monitor."""

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json

import pandas as pd
import streamlit as st
import yaml

from ui.layout import page_chrome, empty_state
from ui.cards import section_header, kpi_card_compact, stat_row
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, RED, YELLOW, ORANGE,
)

TARGETS = ["total_energy_kwh", "cooling_demand_kw", "water_consumption_l"]


def _status_dot(status: str) -> tuple[str, str]:
    """Return (color, label) for a status level."""
    mapping = {
        "healthy": (GREEN, "HEALTHY"),
        "warning": (YELLOW, "WARNING"),
        "error": (RED, "ERROR"),
        "unavailable": (TEXT_MUTED, "N/A"),
    }
    return mapping.get(status, (TEXT_MUTED, "N/A"))


def _status_card(name: str, status: str, details: str, icon: str = ""):
    """Render a system component status card."""
    color, label = _status_dot(status)
    icon_html = f"{icon} " if icon else ""
    st.markdown(
        f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.6rem">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem">
                <span style="font-weight:700;font-size:0.92rem;color:{TEXT}">{icon_html}{name}</span>
                <span style="background:{color}18;color:{color};border:1px solid {color}40;border-radius:20px;padding:0.12rem 0.6rem;font-size:0.68rem;font-weight:700;letter-spacing:0.06em">{label}</span>
            </div>
            <div style="color:{TEXT_MUTED};font-size:0.8rem">{details}</div>
        </div>""",
        unsafe_allow_html=True,
    )


page_chrome(
    "System Health",
    "Prototype system component status and operational readiness",
    "🔧",
)

# ── Section: System Components ───────────────────────────────────────────────

section_header("System Components", "Status of each subsystem in the prototype", "⚙️")

col1, col2 = st.columns(2)

# --- Data Pipeline ---
with col1:
    data_path = Path("data/generated/data_centre_hourly.csv")
    if data_path.exists():
        try:
            df = pd.read_csv(data_path, low_memory=False)
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            row_count = len(df)
            latest = df["timestamp"].max().strftime("%Y-%m-%d %H:%M") if not df["timestamp"].isna().all() else "Unknown"
            _status_card(
                "Data Pipeline", "healthy",
                f"{row_count:,} rows · Latest: {latest}",
                icon="📊",
            )
        except Exception:
            _status_card("Data Pipeline", "error", "File exists but cannot be loaded", icon="📊")
    else:
        _status_card("Data Pipeline", "error", "data_centre_hourly.csv not found", icon="📊")

# --- Forecast Models ---
with col2:
    models_loaded = 0
    model_details = []
    for t in TARGETS:
        joblib_path = Path(f"models/forecasting/{t}.joblib")
        meta_path = Path(f"models/metadata/{t}.json")
        if joblib_path.exists() and meta_path.exists():
            models_loaded += 1
            try:
                meta = json.loads(meta_path.read_text())
                model_details.append(f"{meta.get('model_name', t)}")
            except Exception:
                model_details.append(t)

    if models_loaded == len(TARGETS):
        _status_card(
            "Forecast Models", "healthy",
            f"{models_loaded}/{len(TARGETS)} models loaded · {', '.join(model_details)}",
            icon="🤖",
        )
    elif models_loaded > 0:
        _status_card(
            "Forecast Models", "warning",
            f"{models_loaded}/{len(TARGETS)} models loaded",
            icon="🤖",
        )
    else:
        _status_card("Forecast Models", "error", "No models found", icon="🤖")

# --- Anomaly Engine ---
with col1:
    try:
        from src.anomaly_detection import detect_anomalies  # noqa: F401
        eval_artifacts = Path("reports/evaluation/anomaly_metrics.json").exists()
        if eval_artifacts:
            _status_card("Anomaly Engine", "healthy", "Module loaded · Evaluation artifacts present", icon="🛡️")
        else:
            _status_card("Anomaly Engine", "warning", "Module loaded · No evaluation artifacts", icon="🛡️")
    except ImportError:
        _status_card("Anomaly Engine", "error", "Module import failed", icon="🛡️")

# --- Recommendation Engine ---
with col2:
    try:
        from src.recommendations import generate_recommendations  # noqa: F401
        _status_card("Recommendation Engine", "healthy", "Module loaded and operational", icon="💡")
    except ImportError:
        _status_card("Recommendation Engine", "unavailable", "Module not available", icon="💡")
    except Exception:
        _status_card("Recommendation Engine", "warning", "Module found but may have issues", icon="💡")

# --- Configuration ---
with col1:
    settings_path = Path("config/settings.yaml")
    thresholds_path = Path("config/thresholds.yaml")
    if settings_path.exists() and thresholds_path.exists():
        try:
            settings = yaml.safe_load(settings_path.read_text())
            thresholds = yaml.safe_load(thresholds_path.read_text())
            _status_card(
                "Configuration", "healthy",
                f"settings.yaml + thresholds.yaml loaded",
                icon="⚙️",
            )
        except Exception:
            _status_card("Configuration", "warning", "Files exist but parsing failed", icon="⚙️")
    else:
        missing = []
        if not settings_path.exists():
            missing.append("settings.yaml")
        if not thresholds_path.exists():
            missing.append("thresholds.yaml")
        _status_card("Configuration", "error", f"Missing: {', '.join(missing)}", icon="⚙️")

# --- Evaluation Reports ---
with col2:
    comparison_exists = Path("reports/evaluation/model_comparison.csv").exists()
    results_exists = Path("reports/FINAL_RESULTS.md").exists()
    if comparison_exists and results_exists:
        _status_card("Evaluation Reports", "healthy", "model_comparison.csv + FINAL_RESULTS.md present", icon="📄")
    elif comparison_exists or results_exists:
        _status_card("Evaluation Reports", "warning", "Partial reports available", icon="📄")
    else:
        _status_card("Evaluation Reports", "error", "No evaluation reports found", icon="📄")

# ── Section: Application Configuration ───────────────────────────────────────

section_header("Application Configuration", "Loaded settings from config/settings.yaml", "🔧")

try:
    settings_path = Path("config/settings.yaml")
    if not settings_path.exists():
        raise FileNotFoundError

    settings = yaml.safe_load(settings_path.read_text())

    if isinstance(settings, dict):
        config_items = []
        for key, val in settings.items():
            if isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    config_items.append((f"{key}.{sub_key}", str(sub_val), ""))
            else:
                config_items.append((key, str(val), ""))

        for i in range(0, len(config_items), 5):
            chunk = config_items[i:i + 5]
            stat_row(chunk)
    else:
        st.info("Configuration file is empty or has unexpected format.")

except Exception:
    empty_state("🔧", "Configuration unavailable", "Cannot load config/settings.yaml")

# ── Section: Artifact Inventory ──────────────────────────────────────────────

section_header("Artifact Inventory", "Existence check for all expected system files", "📂")

artifacts = {
    "Data": [
        ("data/generated/data_centre_hourly.csv", "Primary dataset"),
    ],
    "Models": [
        (f"models/forecasting/{t}.joblib", f"{t} model") for t in TARGETS
    ] + [
        (f"models/metadata/{t}.json", f"{t} metadata") for t in TARGETS
    ] + [
        ("models/anomaly_detection/isolation_forest.joblib", "Anomaly model"),
    ],
    "Reports": [
        ("reports/evaluation/model_comparison.csv", "Model comparison"),
        ("reports/FINAL_RESULTS.md", "Final results"),
        ("reports/evaluation/anomaly_metrics.json", "Anomaly metrics"),
        ("reports/evaluation/data_quality_report.csv", "Data quality report"),
    ],
    "Configuration": [
        ("config/settings.yaml", "App settings"),
        ("config/thresholds.yaml", "Alert thresholds"),
    ],
}

for category, files in artifacts.items():
    st.markdown(
        f'<div style="color:{TEXT_SECONDARY};font-size:0.78rem;font-weight:600;letter-spacing:0.08em;'
        f'text-transform:uppercase;margin-top:1rem;margin-bottom:0.4rem">{category}</div>',
        unsafe_allow_html=True,
    )
    for file_path, description in files:
        exists = Path(file_path).exists()
        dot_color = GREEN if exists else RED
        status_label = "Found" if exists else "Missing"
        st.markdown(
            f"""<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;padding:0.5rem 0.8rem;margin-bottom:0.3rem;display:flex;align-items:center;gap:0.6rem;font-size:0.82rem">
                <span style="color:{dot_color}">●</span>
                <span style="color:{TEXT};flex:1">{description}</span>
                <span style="color:{TEXT_MUTED};font-size:0.72rem;font-family:monospace">{file_path}</span>
                <span style="color:{dot_color};font-size:0.68rem;font-weight:600">{status_label}</span>
            </div>""",
            unsafe_allow_html=True,
        )
