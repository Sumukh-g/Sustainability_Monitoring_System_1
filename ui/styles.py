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
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {BG_DARK} !important;
    color: {TEXT} !important;
    font-family: {FONT_STACK} !important;
}}
.stApp {{
    overflow-x: hidden !important;
}}

/* Keep Streamlit header for sidebar reopen; hide chrome noise only */
.stApp > header,
header[data-testid="stHeader"] {{
    display: block !important;
    visibility: visible !important;
    background: {BG_DARK} !important;
    height: 3rem !important;
    z-index: 1000000 !important;
    border-bottom: 1px solid transparent !important;
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
    color: {TEXT} !important;
    background: {BG_CARD} !important;
    border: 1px solid {BORDER_LIGHT} !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebarCollapseButton"] {{
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 1000001 !important;
}}

/* Main content: avoid sidebar collision and cramped edges */
.block-container {{
    padding: 2.6rem 1.75rem 2.5rem 1.75rem !important;
    max-width: 1440px !important;
    overflow-x: hidden !important;
}}
section.main > div {{
    overflow-x: hidden !important;
}}
[data-testid="stMain"] {{
    overflow-x: hidden !important;
}}
.stMarkdown, .stMarkdown p, .stMarkdown div, .eco-card, .eco-hero, .eco-value, .eco-value-sm {{
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1117 0%, #0a0e14 100%) !important;
    border-right: 1px solid {BORDER_LIGHT} !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    background: transparent !important;
}}
[data-testid="stSidebar"] .block-container {{
    padding: 0.85rem 0.85rem 2rem 0.85rem !important;
    overflow-x: hidden !important;
}}
[data-testid="stSidebar"] [data-testid="stMarkdown"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {{
    color: {TEXT_SECONDARY} !important;
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
    margin-top: 1.1rem !important;
    margin-bottom: 0.35rem !important;
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
    gap: 0.35rem !important;
}}
[data-testid="stSidebar"] [data-baseweb="radio"] {{
    margin-right: 0.1rem !important;
}}

/* Sidebar nav links — readable contrast */
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"],
[data-testid="stSidebarNav"] a {{
    color: #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 0.42rem 0.65rem !important;
    font-size: 0.86rem !important;
    transition: all 0.15s ease;
    white-space: normal !important;
    line-height: 1.3 !important;
    margin-bottom: 0.15rem !important;
}}
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] span,
[data-testid="stSidebarNav"] a span {{
    color: inherit !important;
}}
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNav"] a:hover {{
    background: rgba(0,212,170,0.08) !important;
    color: {TEXT} !important;
}}
[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"][aria-current="page"],
[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: rgba(0,212,170,0.14) !important;
    color: {GREEN} !important;
    font-weight: 600;
    border-left: 2px solid {GREEN} !important;
}}

/* Page search / home label */
[data-testid="stSidebarNav"] input,
[data-testid="stSidebar"] input[type="text"] {{
    color: {TEXT} !important;
    background: {BG_CARD} !important;
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
    font-size: 1.45rem !important;
}}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    font-size: 0.78rem !important;
}}

/* ── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0.15rem;
    background: {BG_CARD};
    border-radius: 10px;
    padding: 4px;
    border: 1px solid {BORDER};
    flex-wrap: wrap !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    color: {TEXT_MUTED};
    font-size: 0.82rem;
    font-weight: 500;
    padding: 0.5rem 0.9rem;
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
    padding: 0.45rem 1.15rem !important;
    transition: all 0.2s ease;
}}
.stButton > button:hover {{
    opacity: 0.92;
    box-shadow: 0 0 16px rgba(0,212,170,0.25);
}}

/* ── Selectbox / inputs ───────────────────────────────────── */
[data-baseweb="select"], [data-baseweb="input"] {{
    border-radius: 8px !important;
}}
[data-baseweb="select"] > div {{
    background: {BG_CARD} !important;
    border-color: {BORDER_LIGHT} !important;
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

/* ── Dataframes / columns / charts ────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: 10px !important;
    overflow: auto !important;
    max-width: 100% !important;
}}
div[data-testid="stHorizontalBlock"] {{
    flex-wrap: wrap !important;
    gap: 0.75rem !important;
    align-items: stretch !important;
}}
div[data-testid="column"] {{
    min-width: min(100%, 160px) !important;
    overflow: visible !important;
    flex: 1 1 160px !important;
}}
div[data-testid="column"] > div {{
    height: auto;
}}

/* Hide Streamlit warning spam that breaks layouts */
[data-testid="stAlert"] {{
    max-width: 100% !important;
    overflow-wrap: anywhere !important;
}}
div[data-testid="stHorizontalBlock"] [data-testid="stAlert"] {{
    font-size: 0.75rem !important;
}}

/* Kill white Plotly / iframe chrome */
.stPlotlyChart, [data-testid="stPlotlyChart"],
.js-plotly-plot, .plot-container, .svg-container {{
    max-width: 100% !important;
    background: transparent !important;
    border-radius: 12px !important;
}}
.stPlotlyChart > div,
[data-testid="stPlotlyChart"] > div {{
    background: transparent !important;
}}
iframe {{
    max-width: 100% !important;
    background: transparent !important;
}}
.modebar-container {{
    right: 0.4rem !important;
}}

/* Exception boxes should not overflow */
[data-testid="stException"], .stException {{
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
    max-width: 100% !important;
}}

/* ── Dividers ─────────────────────────────────────────────── */
hr {{
    border-color: {BORDER} !important;
    margin: 1.35rem 0 !important;
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

/* st.html wrappers */
[data-testid="stHtml"], .stHtml {{
    width: 100% !important;
}}

/* ── Custom class helpers ─────────────────────────────────── */
.eco-hero {{
    background: linear-gradient(135deg, rgba(0,212,170,0.08) 0%, rgba(0,180,216,0.06) 100%);
    border: 1px solid rgba(0,212,170,0.15);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    overflow: hidden;
    max-width: 100%;
}}
.eco-hero h1 {{
    color: {TEXT};
    font-size: clamp(1.2rem, 2vw, 1.7rem);
    font-weight: 800;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.01em;
    overflow-wrap: anywhere;
    line-height: 1.25;
}}
.eco-hero p {{
    color: {TEXT_SECONDARY};
    font-size: 0.9rem;
    margin: 0;
    overflow-wrap: anywhere;
    line-height: 1.45;
}}

.eco-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.05rem 1.1rem;
    margin-bottom: 0.55rem;
    overflow: visible;
    max-width: 100%;
    box-sizing: border-box;
}}
[data-testid="stHtml"] .eco-card,
.stHtml .eco-card {{
    overflow: visible;
}}
.eco-card-highlight {{
    background: {BG_CARD};
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 12px;
    padding: 1.05rem 1.1rem;
    margin-bottom: 0.55rem;
    box-shadow: 0 0 20px rgba(0,212,170,0.04);
    overflow: hidden;
    max-width: 100%;
    box-sizing: border-box;
}}

.eco-label {{
    color: {TEXT_MUTED};
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 0.3rem;
    overflow-wrap: anywhere;
    line-height: 1.3;
}}
.eco-value {{
    color: {TEXT};
    font-size: clamp(1.05rem, 1.7vw, 1.45rem);
    font-weight: 700;
    line-height: 1.25;
    overflow-wrap: anywhere;
}}
.eco-value-sm {{
    color: {TEXT};
    font-size: clamp(0.92rem, 1.3vw, 1.08rem);
    font-weight: 600;
    overflow-wrap: anywhere;
    line-height: 1.3;
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
    padding: 0.18rem 0.55rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    line-height: 1.2;
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
    margin-top: 1.55rem;
    margin-bottom: 0.55rem;
}}
.eco-section h2 {{
    color: {TEXT};
    font-size: clamp(1.02rem, 1.5vw, 1.15rem);
    font-weight: 700;
    margin: 0 0 0.25rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    line-height: 1.3;
}}
.eco-section p {{
    color: {TEXT_MUTED};
    font-size: 0.82rem;
    margin: 0;
    line-height: 1.4;
}}

.eco-insight {{
    background: {BG_CARD};
    border-left: 3px solid {CYAN};
    border-radius: 0 10px 10px 0;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    color: {TEXT_SECONDARY};
    font-size: 0.85rem;
    line-height: 1.45;
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
    padding: 0.65rem 1rem;
    display: flex;
    align-items: flex-start;
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
    margin-top: 0.35rem;
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
    font-size: 1.15rem;
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
    padding: 1rem 1.15rem;
    margin-bottom: 0.7rem;
}}
.eco-incident-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 0.5rem;
}}

.eco-gauge-ring {{
    position: relative;
    width: 200px;
    height: 200px;
    margin: 0 auto;
}}

/* Responsive comfort */
@media (max-width: 1100px) {{
    .block-container {{
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }}
    .eco-card {{
        padding: 0.9rem !important;
    }}
}}
</style>
"""


def inject_styles():
    """Inject the global EcoNexus CSS. Call once per page."""
    st.markdown(_CSS, unsafe_allow_html=True)
