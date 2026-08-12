"""EcoNexus AI — Design tokens and Plotly template."""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.io as pio

# ── Colour palette ──────────────────────────────────────────────────
BG_DARK = "#0a0a0a"
BG_CARD = "#111111"
BG_CARD_HOVER = "#161616"
BG_SURFACE = "#0f0f0f"
BORDER = "#1e1e1e"
BORDER_LIGHT = "#2a2a2a"

GREEN = "#00d4aa"
GREEN_DIM = "#00a88a"
GREEN_GLOW = "rgba(0,212,170,0.12)"
CYAN = "#00b4d8"
CYAN_DIM = "#0090b0"
BLUE = "#3b82f6"
ORANGE = "#ff6b35"
RED = "#ff3366"
YELLOW = "#fbbf24"
PURPLE = "#a78bfa"

TEXT = "#f1f5f9"
TEXT_SECONDARY = "#94a3b8"
TEXT_MUTED = "#64748b"
TEXT_DIM = "#475569"

STATUS_OPTIMAL = GREEN
STATUS_GOOD = "#22c55e"
STATUS_WARNING = YELLOW
STATUS_ELEVATED = ORANGE
STATUS_CRITICAL = RED

CHART_COLORS = [GREEN, CYAN, BLUE, ORANGE, PURPLE, YELLOW, RED, "#ec4899", "#06b6d4"]

FONT_STACK = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

# ── Plotly template ─────────────────────────────────────────────────

_layout = go.Layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT_STACK, color=TEXT_SECONDARY, size=12),
    title=dict(font=dict(size=15, color=TEXT), x=0, xanchor="left"),
    margin=dict(l=48, r=24, t=48, b=40),
    xaxis=dict(
        gridcolor=BORDER,
        zerolinecolor=BORDER,
        linecolor=BORDER,
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor=BORDER,
        zerolinecolor=BORDER,
        linecolor=BORDER,
        tickfont=dict(size=11),
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color=TEXT_SECONDARY),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
    colorway=CHART_COLORS,
    hoverlabel=dict(
        bgcolor=BG_CARD,
        font_size=12,
        font_family=FONT_STACK,
        font_color=TEXT,
        bordercolor=BORDER_LIGHT,
    ),
    hovermode="x unified",
)

ECO_TEMPLATE = go.layout.Template(layout=_layout)
pio.templates["econexus"] = ECO_TEMPLATE
pio.templates.default = "econexus"


def severity_color(severity: str) -> str:
    return {
        "Critical": RED,
        "High": ORANGE,
        "Medium": YELLOW,
        "Low": CYAN,
        "Informational": TEXT_MUTED,
    }.get(severity, TEXT_MUTED)


def score_color(score: float) -> str:
    if score >= 85:
        return GREEN
    if score >= 70:
        return STATUS_GOOD
    if score >= 50:
        return YELLOW
    if score >= 30:
        return ORANGE
    return RED


def score_label(score: float) -> str:
    if score >= 85:
        return "EXCELLENT"
    if score >= 70:
        return "GOOD"
    if score >= 50:
        return "MODERATE"
    if score >= 30:
        return "POOR"
    return "CRITICAL"


def pue_status(pue: float) -> tuple[str, str]:
    if pue < 1.2:
        return "OPTIMAL", GREEN
    if pue < 1.5:
        return "GOOD", STATUS_GOOD
    if pue < 1.8:
        return "ELEVATED", YELLOW
    return "CRITICAL", RED
