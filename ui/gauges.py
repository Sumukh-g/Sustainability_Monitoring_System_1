"""EcoNexus AI — Gauge components."""

from __future__ import annotations
import plotly.graph_objects as go
import streamlit as st
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_MUTED, GREEN, GREEN_DIM,
    CYAN, YELLOW, ORANGE, RED,
    score_color, score_label,
)


def sustainability_gauge(score: float, height: int = 260):
    """Hero sustainability gauge — the dominant visual on the Command Center."""
    color = score_color(score)
    label = score_label(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(
            font=dict(size=52, color=TEXT, weight=800),
            suffix="",
        ),
        gauge=dict(
            axis=dict(range=[0, 100], visible=False),
            bar=dict(color=color, thickness=0.82),
            bgcolor="rgba(30,30,30,0.5)",
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
        margin=dict(l=30, r=30, t=20, b=20),
        annotations=[
            dict(
                text=f"<b>{label}</b>",
                x=0.5, y=0.15,
                font=dict(size=13, color=color),
                showarrow=False,
                xref="paper", yref="paper",
            ),
            dict(
                text="SUSTAINABILITY SCORE",
                x=0.5, y=-0.02,
                font=dict(size=10, color=TEXT_MUTED),
                showarrow=False,
                xref="paper", yref="paper",
            ),
        ],
    )
    return fig


def efficiency_mini_gauge(value: float, label: str, max_val: float = 100, height: int = 150):
    """Smaller efficiency sub-gauge for Energy/Water/Carbon/Cooling."""
    color = score_color(value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(font=dict(size=24, color=TEXT, weight=700), suffix="%"),
        title=dict(text=label, font=dict(size=10, color=TEXT_MUTED)),
        gauge=dict(
            axis=dict(range=[0, max_val], visible=False),
            bar=dict(color=color, thickness=0.75),
            bgcolor="rgba(30,30,30,0.4)",
            borderwidth=0,
        ),
    ))
    fig.update_layout(height=height, margin=dict(l=20, r=20, t=35, b=5))
    return fig


def pue_gauge(pue: float, height: int = 180):
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
        number=dict(font=dict(size=28, color=TEXT, weight=700), valueformat=".2f"),
        title=dict(text="PUE", font=dict(size=10, color=TEXT_MUTED)),
        gauge=dict(
            axis=dict(range=[1.0, 2.5], tickfont=dict(size=9, color=TEXT_MUTED)),
            bar=dict(color=color, thickness=0.7),
            bgcolor="rgba(30,30,30,0.4)",
            borderwidth=0,
            steps=[
                dict(range=[1.0, 1.2], color="rgba(0,212,170,0.08)"),
                dict(range=[1.2, 1.5], color="rgba(34,197,94,0.06)"),
                dict(range=[1.5, 1.8], color="rgba(251,191,36,0.06)"),
                dict(range=[1.8, 2.5], color="rgba(255,51,102,0.06)"),
            ],
        ),
    ))
    fig.update_layout(height=height, margin=dict(l=20, r=20, t=30, b=5))
    return fig
