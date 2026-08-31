"""EcoNexus AI — Global CSS injection."""

from __future__ import annotations
import streamlit as st
from ui.theme import (
    BG_DARK, BG_CARD, BG_SURFACE, BORDER, BORDER_LIGHT,
    GREEN, GREEN_DIM, GREEN_GLOW, CYAN, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    FONT_STACK, RED, ORANGE, YELLOW,
)

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global reset ─────────────────────────────────────────── */
html, body, .stApp {{
    background-color: {BG_DARK} !important;
    color: {TEXT} !important;
    font-family: {FONT_STACK} !important;
    overflow-x: hidden !important;
}}
/* Keep Streamlit header visible so the sidebar reopen control works.
   Hide only chrome/menu noise, not the collapsed-control button. */
.stApp > header,
header[data-testid="stHeader"] {{
    display: block !important;
    visibility: visible !important;
    background: transparent !important;
    height: 3.25rem !important;
    z-index: 1000000 !important;
}}
#MainMenu {{visibility: hidden !important;}}
footer {{display: none !important;}}
[data-testid="stToolbar"] {{visibility: hidden !important; height: 0 !important;}}
[data-testid="stDecoration"] {{display: none !important;}}
[data-testid="stStatusWidget"] {{visibility: hidden !important;}}

/* Explicitly keep sidebar expand/collapse controls clickable */
[data-testid="collapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"],
button[kind="header"],
button[data-testid="baseButton-header"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 1000001 !important;
    position: relative !important;
    color: {TEXT} !important;
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebarCollapseButton"] {{
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 1000001 !important;
}}

.block-container {{
    padding: 3.5rem 1.5rem 2rem 1.5rem !important;
    max-width: 1400px !important;
    overflow-x: hidden !important;
}}
section.main > div {{
    overflow-x: hidden !important;
}}
.stMarkdown, .stMarkdown p, .stMarkdown div, .eco-card, .eco-hero, .eco-value, .eco-value-sm {{
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1117 0%, #0a0e14 100%) !important;
    border-right: 1px solid {BORDER} !important;
    z-index: 999990 !important;
}}
[data-testid="stSidebar"][aria-expanded="true"] {{
    min-width: 18rem !important;
}}
[data-testid="stSidebar"] .block-container {{
    padding: 1rem 0.8rem 2rem 0.8rem !important;
    overflow-x: hidden !important;
}}
[data-testid="stSidebar"] [data-testid="stMarkdown"] p {{
    color: {TEXT_SECONDARY} !important;
    font-size: 0.82rem !important;
}}
[data-testid="stSidebar"] h1 {{
    font-size: 1.1rem !important;
    color: {GREEN} !important;
    letter-spacing: 0.08em;
    font-weight: 700;
}}
[data-testid="stSidebar"] h2 {{
    font-size: 0.72rem !important;
    color: {TEXT_MUTED} !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 1.2rem !important;
    margin-bottom: 0.3rem !important;
    font-weight: 600;
    padding-left: 0.2rem;
}}
[data-testid="stSidebar"] h3 {{
    font-size: 0.78rem !important;
    color: {TEXT_SECONDARY} !important;
    font-weight: 500;
}}
/* Period radio chips: wrap instead of overlapping */
[data-testid="stSidebar"] [role="radiogroup"] {{
    flex-wrap: wrap !important;
    gap: 0.25rem !important;
}}
[data-testid="stSidebar"] [data-baseweb="radio"] {{
    margin-right: 0.15rem !important;
}}
/* Sidebar nav links */
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {{
    color: {TEXT_SECONDARY} !important;
    border-radius: 8px !important;
    padding: 0.35rem 0.6rem !important;
    font-size: 0.85rem !important;
    transition: all 0.15s ease;
    white-space: normal !important;
    line-height: 1.25 !important;
}}
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {{
    background: rgba(0,212,170,0.06) !important;
    color: {TEXT} !important;
}}
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"] {{
    background: rgba(0,212,170,0.1) !important;
    color: {GREEN} !important;
    font-weight: 600;
    border-left: 2px solid {GREEN} !important;
}}

/* ── Metric cards ─────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}}
[data-testid="stMetric"] label {{
    color: {TEXT_MUTED} !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {TEXT} !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    font-size: 0.78rem !important;
}}

/* ── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: {BG_CARD};
    border-radius: 10px;
    padding: 4px;
    border: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    color: {TEXT_MUTED};
    font-size: 0.82rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
}}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: rgba(0,212,170,0.1);
    color: {GREEN};
    font-weight: 600;
}}
.stTabs [data-baseweb="tab-highlight"] {{
    background-color: {GREEN} !important;
}}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {{
    background: linear-gradient(135deg, {GREEN_DIM}, {GREEN}) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s ease;
}}
.stButton > button:hover {{
    opacity: 0.9;
    box-shadow: 0 0 16px rgba(0,212,170,0.25);
}}

/* ── Selectbox / inputs ───────────────────────────────────── */
[data-baseweb="select"], [data-baseweb="input"] {{
    border-radius: 8px !important;
}}
[data-baseweb="select"] > div {{
    background: {BG_CARD} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
}}

/* ── Expanders ────────────────────────────────────────────── */
[data-testid="stExpander"] {{
    background: {BG_CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}
[data-testid="stExpander"] summary {{
    color: {TEXT} !important;
    font-weight: 500;
}}

/* ── Dataframes ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: 10px !important;
    overflow: auto !important;
    max-width: 100% !important;
}}
div[data-testid="stHorizontalBlock"] {{
    flex-wrap: wrap !important;
    gap: 0.5rem !important;
}}
div[data-testid="column"] {{
    min-width: 0 !important;
    overflow: hidden !important;
}}
.stPlotlyChart, [data-testid="stPlotlyChart"] {{
    max-width: 100% !important;
    overflow: hidden !important;
}}
iframe {{
    max-width: 100% !important;
}}

/* ── Dividers ─────────────────────────────────────────────── */
hr {{
    border-color: {BORDER} !important;
    margin: 1.5rem 0 !important;
}}

/* ── Multiselect ──────────────────────────────────────────── */
[data-baseweb="tag"] {{
    background: rgba(0,212,170,0.15) !important;
    border: 1px solid rgba(0,212,170,0.3) !important;
    color: {GREEN} !important;
    border-radius: 6px !important;
}}

/* ── Slider ───────────────────────────────────────────────── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{
    background: {GREEN} !important;
}}

/* ── Custom class helpers ─────────────────────────────────── */
.eco-hero {{
    background: linear-gradient(135deg, rgba(0,212,170,0.08) 0%, rgba(0,180,216,0.06) 100%);
    border: 1px solid rgba(0,212,170,0.15);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
    max-width: 100%;
}}
.eco-hero h1 {{
    color: {TEXT};
    font-size: clamp(1.25rem, 2.2vw, 1.8rem);
    font-weight: 800;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.01em;
    overflow-wrap: anywhere;
}}
.eco-hero p {{
    color: {TEXT_SECONDARY};
    font-size: 0.92rem;
    margin: 0;
    overflow-wrap: anywhere;
}}

.eco-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    overflow: hidden;
    max-width: 100%;
}}
.eco-card-highlight {{
    background: {BG_CARD};
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 20px rgba(0,212,170,0.04);
    overflow: hidden;
    max-width: 100%;
}}

.eco-label {{
    color: {TEXT_MUTED};
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 0.3rem;
    overflow-wrap: anywhere;
}}
.eco-value {{
    color: {TEXT};
    font-size: clamp(1.05rem, 1.8vw, 1.5rem);
    font-weight: 700;
    line-height: 1.25;
    overflow-wrap: anywhere;
}}
.eco-value-sm {{
    color: {TEXT};
    font-size: clamp(0.95rem, 1.4vw, 1.1rem);
    font-weight: 600;
    overflow-wrap: anywhere;
}}
.eco-delta {{
    font-size: 0.78rem;
    font-weight: 500;
    margin-top: 0.25rem;
}}
.eco-delta-pos {{ color: {GREEN}; }}
.eco-delta-neg {{ color: {RED}; }}
.eco-delta-neutral {{ color: {TEXT_MUTED}; }}

.eco-status {{
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}
.eco-status-optimal {{
    background: rgba(0,212,170,0.12);
    color: {GREEN};
    border: 1px solid rgba(0,212,170,0.25);
}}
.eco-status-good {{
    background: rgba(34,197,94,0.12);
    color: #22c55e;
    border: 1px solid rgba(34,197,94,0.25);
}}
.eco-status-warning {{
    background: rgba(251,191,36,0.12);
    color: {YELLOW};
    border: 1px solid rgba(251,191,36,0.25);
}}
.eco-status-elevated {{
    background: rgba(255,107,53,0.12);
    color: {ORANGE};
    border: 1px solid rgba(255,107,53,0.25);
}}
.eco-status-critical {{
    background: rgba(255,51,102,0.12);
    color: {RED};
    border: 1px solid rgba(255,51,102,0.25);
}}

.eco-section {{
    margin-top: 1.8rem;
    margin-bottom: 0.5rem;
}}
.eco-section h2 {{
    color: {TEXT};
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 0.2rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.eco-section p {{
    color: {TEXT_MUTED};
    font-size: 0.82rem;
    margin: 0;
}}

.eco-insight {{
    background: {BG_CARD};
    border-left: 3px solid {CYAN};
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    color: {TEXT_SECONDARY};
    font-size: 0.85rem;
}}
.eco-insight-warn {{
    border-left-color: {ORANGE};
}}
.eco-insight-crit {{
    border-left-color: {RED};
}}

.eco-alert-strip {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.4rem;
    font-size: 0.83rem;
    color: {TEXT_SECONDARY};
}}
.eco-alert-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}}

.eco-twin-node {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
}}
.eco-twin-node h4 {{
    color: {TEXT_MUTED};
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0 0 0.3rem 0;
    font-weight: 600;
}}
.eco-twin-node .eco-twin-val {{
    color: {TEXT};
    font-size: 1.2rem;
    font-weight: 700;
}}
.eco-twin-arrow {{
    text-align: center;
    color: {GREEN};
    font-size: 1.1rem;
    padding: 0.2rem 0;
}}

.eco-incident {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
}}
.eco-incident-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}}

.eco-gauge-ring {{
    position: relative;
    width: 200px;
    height: 200px;
    margin: 0 auto;
}}
</style>
"""


def inject_styles():
    """Inject the global EcoNexus CSS. Call once per page."""
    st.markdown(_CSS, unsafe_allow_html=True)
