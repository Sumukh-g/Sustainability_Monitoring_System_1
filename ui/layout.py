"""EcoNexus AI — Layout helpers and page shell."""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
import yaml

from ui.styles import inject_styles
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, RED, ORANGE, YELLOW,
)

TEXT_DIM = "#475569"

from src.data_loader import load_data


PRODUCT_NAME = "EcoNexus AI"
PRODUCT_SUBTITLE = "Intelligent Sustainability Command Center"
VERSION = "1.0.0"


def page_config(title: str, icon: str = "🌿"):
    """Set Streamlit page config with EcoNexus defaults."""
    st.set_page_config(
        page_title=f"{title} — {PRODUCT_NAME}",
        page_icon=icon,
        layout="wide",
    )


def page_chrome(title: str, subtitle: str = "", icon: str = ""):
    """Inject styles and render the page hero header."""
    inject_styles()
    _sidebar_branding()
    icon_html = f"{icon} " if icon else ""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.html(f'<div class="eco-hero"><h1>{icon_html}{title}</h1>{sub}</div>')


def _sidebar_branding():
    """Render sidebar product identity and status."""
    with st.sidebar:
        st.html(
            f'<div style="text-align:center;padding:0.45rem 0 0.7rem 0">'
            f'<div style="font-size:1.25rem;font-weight:800;color:{GREEN};letter-spacing:0.05em">'
            f'{PRODUCT_NAME}</div>'
            f'<div style="font-size:0.7rem;color:{TEXT_SECONDARY};letter-spacing:0.06em;'
            f'text-transform:uppercase;margin-top:0.2rem;line-height:1.35">{PRODUCT_SUBTITLE}</div>'
            f'</div>'
        )
        st.markdown("---")


@st.cache_data
def get_data(path: str = "data/generated/data_centre_hourly.csv") -> pd.DataFrame:
    return load_data(path)


@st.cache_data
def get_config():
    return (
        yaml.safe_load(Path("config/settings.yaml").read_text()),
        yaml.safe_load(Path("config/thresholds.yaml").read_text()),
    )


def global_filters(show_aggregation: bool = True):
    """Render sidebar filters and return filtered data + aggregation choice."""
    data = get_data()
    with st.sidebar:
        st.markdown("## Filters")
        sites = st.multiselect(
            "Site",
            sorted(data.site.unique()),
            default=sorted(data.site.unique()),
            key="global_site",
        )
        mn, mx = data.timestamp.min().date(), data.timestamp.max().date()
        # Vertical presets avoid cramped chip overlap in the narrow sidebar
        preset = st.radio(
            "Period",
            ["24H", "7D", "30D", "90D", "1Y", "Custom"],
            index=2,
            horizontal=False,
            key="time_preset",
        )
        if preset == "Custom":
            dates = st.date_input(
                "Date range",
                (max(mn, mx - pd.Timedelta(days=30)), mx),
                min_value=mn,
                max_value=mx,
                key="global_dates",
            )
        else:
            days = {"24H": 1, "7D": 7, "30D": 30, "90D": 90, "1Y": 366}[preset]
            end = mx
            start = max(mn, end - pd.Timedelta(days=days))
            dates = (start, end)

        agg = "Hourly"
        if show_aggregation:
            agg = st.selectbox(
                "Aggregation", ["Hourly", "Daily", "Weekly", "Monthly"],
                index=0, key="global_agg",
            )

        st.markdown("---")
        _sidebar_system_status()
        st.html(
            f'<div style="text-align:center;color:{TEXT_DIM};font-size:0.68rem;padding-top:1rem">v{VERSION}</div>'
        )

    if len(dates) != 2:
        st.warning("Select a valid date range.")
        return data.iloc[0:0], agg

    start_ts = pd.Timestamp(dates[0])
    end_ts = pd.Timestamp(dates[1]) + pd.Timedelta(days=1)
    filtered = data[
        data.site.isin(sites) & data.timestamp.between(start_ts, end_ts, inclusive="left")
    ]
    if filtered.empty:
        st.info("No observations match these filters. Adjust the site or date range.")
    return filtered, agg


def _sidebar_system_status():
    """Show system health summary in sidebar."""
    from pathlib import Path
    models_ok = all(
        Path(f"models/forecasting/{t}.joblib").exists()
        for t in ("total_energy_kwh", "cooling_demand_kw", "water_consumption_l")
    )
    data_ok = Path("data/generated/data_centre_hourly.csv").exists()

    def dot(ok: bool) -> str:
        c = GREEN if ok else RED
        return f'<span style="color:{c};font-size:0.7rem">●</span>'

    st.markdown("## System")
    st.html(
        f'<div style="font-size:0.8rem;color:{TEXT_SECONDARY};line-height:1.75">'
        f'{dot(data_ok)} Data pipeline<br>'
        f'{dot(models_ok)} Forecast models<br>'
        f'{dot(True)} Anomaly engine<br>'
        f'{dot(True)} Recommendation engine</div>'
    )


def empty_state(icon: str, title: str, message: str = ""):
    """Professional empty/loading state."""
    msg = (
        f'<div style="color:{TEXT_MUTED};font-size:0.85rem;margin-top:0.35rem;line-height:1.4">{message}</div>'
        if message else ""
    )
    st.html(
        f'<div style="text-align:center;padding:3rem 1rem;color:{TEXT_SECONDARY}">'
        f'<div style="font-size:2.5rem;margin-bottom:0.5rem">{icon}</div>'
        f'<div style="font-size:1rem;font-weight:600;color:{TEXT}">{title}</div>{msg}</div>'
    )
