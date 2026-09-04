"""EcoNexus AI — Gauge components."""

from __future__ import annotations
import plotly.graph_objects as go
from ui.theme import (
    TEXT, TEXT_MUTED, GREEN,
    YELLOW, RED,
    score_color, score_label,
)


def sustainability_gauge(score: float, height: int = 280):
    """Hero sustainability gauge — the dominant visual on the Command Center."""
    color = score_color(score)
    label = score_label(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(
            font=dict(size=48, color=TEXT),
            valueformat=".0f",
        ),
        title=dict(
            text=f"<b style='color:{color}'>{label}</b><br>"
                 f"<span style='font-size:11px;color:{TEXT_MUTED}'>SUSTAINABILITY SCORE</span>",
            font=dict(size=14, color=color),
        ),
        gauge=dict(
            axis=dict(range=[0, 100], visible=False),
            bar=dict(color=color, thickness=0.82),
            bgcolor="rgba(17,17,17,0.9)",
            borderwidth=0,
            steps=[
                dict(range=[0, 30], color="rgba(255,51,102,0.08)"),
                dict(range=[30, 50], color="rgba(255,107,53,0.06)"),
                dict(range=[50, 70], color="rgba(251,191,36,0.06)"),
                dict(range=[70, 85], color="rgba(34,197,94,0.06)"),
                dict(range=[85, 100], color="rgba(0,212,170,0.08)"),
            ],
            threshold=dict(
                line=dict(color=color, width=3),
                thickness=0.85,
                value=score,
            ),
        ),
    ))
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=24, r=24, t=56, b=16),
        font=dict(color=TEXT),
    )
    return fig


def efficiency_mini_gauge(value: float, label: str, max_val: float = 100, height: int = 160):
    """Smaller efficiency sub-gauge for Energy/Water/Carbon/Cooling."""
    color = score_color(value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(font=dict(size=22, color=TEXT), suffix="%"),
        title=dict(text=label, font=dict(size=11, color=TEXT_MUTED)),
        gauge=dict(
            axis=dict(range=[0, max_val], visible=False),
            bar=dict(color=color, thickness=0.75),
            bgcolor="rgba(17,17,17,0.85)",
            borderwidth=0,
        ),
    ))
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=12, r=12, t=40, b=8),
        font=dict(color=TEXT),
    )
    return fig


def pue_gauge(pue: float, height: int = 190):
    """PUE-specific gauge (lower is better, range 1.0-2.5)."""
    if pue < 1.2:
        color = GREEN
    elif pue < 1.5:
        color = "#22c55e"
    elif pue < 1.8:
        color = YELLOW
    else:
        color = RED

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pue,
        number=dict(font=dict(size=26, color=TEXT), valueformat=".2f"),
        title=dict(text="PUE", font=dict(size=11, color=TEXT_MUTED)),
        gauge=dict(
            axis=dict(range=[1.0, 2.5], tickfont=dict(size=9, color=TEXT_MUTED)),
            bar=dict(color=color, thickness=0.7),
            bgcolor="rgba(17,17,17,0.85)",
            borderwidth=0,
            steps=[
                dict(range=[1.0, 1.2], color="rgba(0,212,170,0.08)"),
                dict(range=[1.2, 1.5], color="rgba(34,197,94,0.06)"),
                dict(range=[1.5, 1.8], color="rgba(251,191,36,0.06)"),
                dict(range=[1.8, 2.5], color="rgba(255,51,102,0.06)"),
            ],
        ),
    ))
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=16, r=16, t=36, b=8),
        font=dict(color=TEXT),
    )
    return fig
