"""EcoNexus AI — Data Explorer."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.layout import page_chrome, global_filters, empty_state
from ui.cards import section_header, stat_row, kpi_card_compact
from ui.charts import show
from ui.theme import GREEN, RED, TEXT_MUTED, TEXT, BG_CARD, BORDER

page_chrome("Data Explorer", "Interactive dataset inspection and quality validation", "🔎")

data, agg = global_filters()

if data.empty:
    empty_state("📭", "No data available", "Adjust filters or ensure the data pipeline has been run.")
    st.stop()

# ── Tabs ─────────────────────────────────────────────────────────────────────

tab_overview, tab_explore, tab_quality, tab_stats = st.tabs(
    ["Overview", "Explore", "Quality", "Statistics"]
)

# ── Overview Tab ─────────────────────────────────────────────────────────────

with tab_overview:
    section_header("Dataset Overview", "High-level summary of loaded data", "📋")

    row_count = f"{len(data):,}"
    col_count = str(len(data.columns))
    date_min = data["timestamp"].min().strftime("%Y-%m-%d") if "timestamp" in data.columns else "—"
    date_max = data["timestamp"].max().strftime("%Y-%m-%d") if "timestamp" in data.columns else "—"
    site_count = str(data["site"].nunique()) if "site" in data.columns else "—"
    anomaly_count = str(int(data["anomaly_ground_truth"].sum())) if "anomaly_ground_truth" in data.columns else "0"

    stat_row([
        ("Rows", row_count, "observations"),
        ("Columns", col_count, "features"),
        ("Date Range", f"{date_min} → {date_max}", ""),
        ("Sites", site_count, "locations"),
        ("Anomalies", anomaly_count, "labelled"),
    ])

# ── Explore Tab ──────────────────────────────────────────────────────────────

with tab_explore:
    section_header("Data Exploration", "Filter and inspect individual columns", "🔍")

    all_cols = list(data.columns)
    selected_cols = st.multiselect(
        "Select columns to display",
        all_cols,
        default=all_cols[:8],
        key="explorer_cols",
    )

    if selected_cols:
        display = data[selected_cols].copy()
        for col in display.select_dtypes(include=["datetime", "datetimetz"]).columns:
            display[col] = display[col].astype(str)
        st.dataframe(display, width="stretch")
        st.download_button(
            "Download filtered CSV",
            data[selected_cols].to_csv(index=False),
            "filtered_data.csv",
            "text/csv",
            key="dl_filtered",
        )
    else:
        st.info("Select at least one column to display.")

# ── Quality Tab ──────────────────────────────────────────────────────────────

with tab_quality:
    section_header("Data Quality Validation", "Automated checks on the current dataset", "✅")

    try:
        from src.data_loader import validate_data

        validation = validate_data(data)

        for _, row in validation.iterrows():
            passed = row["passed"]
            dot_color = GREEN if passed else RED
            status_text = "PASS" if passed else "FAIL"
            count_info = f" ({row['count']} issues)" if not passed and row["count"] > 0 else ""

            st.html(
                f'<div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;'
                f'padding:0.8rem 1rem;margin-bottom:0.5rem;display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap">'
                f'<span style="color:{dot_color};font-size:1.2rem">●</span>'
                f'<div style="flex:1;min-width:160px">'
                f'<div style="font-weight:600;color:{TEXT};font-size:0.9rem">{row["check"].replace("_", " ").title()}</div>'
                f'<div style="color:{TEXT_MUTED};font-size:0.78rem;line-height:1.35">{row["detail"]}{count_info}</div>'
                f'</div>'
                f'<span style="color:{dot_color};font-size:0.72rem;font-weight:700;letter-spacing:0.08em">{status_text}</span></div>'
            )

    except Exception as e:
        empty_state("✅", "Validation unavailable", str(e))

# ── Statistics Tab ───────────────────────────────────────────────────────────

with tab_stats:
    section_header("Descriptive Statistics", "Summary statistics for numeric columns", "📊")

    try:
        desc = data.describe(include="all").T
        display_desc = desc.copy()
        for col in display_desc.select_dtypes(include=["datetime", "datetimetz"]).columns:
            display_desc[col] = display_desc[col].astype(str)
        display_desc = display_desc.fillna("—").astype(str)
        st.dataframe(display_desc, width="stretch")
    except Exception as e:
        empty_state("📊", "Statistics unavailable", str(e))
