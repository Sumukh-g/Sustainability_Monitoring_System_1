"""EcoNexus AI — Standardised chart functions."""

from __future__ import annotations
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, BLUE, ORANGE, RED, YELLOW, PURPLE,
    CHART_COLORS,
)


def _hex_to_rgba(hex_color: str, alpha: float = 0.25) -> str:
    """Convert hex color to rgba string for Plotly fill colors."""
    h = hex_color.lstrip("#")
    if len(h) == 6:
        r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"
    return f"rgba(100,100,100,{alpha})"


def _chart_layout(fig: go.Figure, title: str = "", height: int = 340) -> go.Figure:
    """Apply consistent spacing so titles and legends do not collide."""
    fig.update_layout(
        title=dict(text=title, y=0.98, pad=dict(b=8)) if title else None,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=52, r=28, t=72 if title else 48, b=44),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig


def trend_line(
    data: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    height: int = 340,
    markers: pd.DataFrame | None = None,
    marker_label: str = "Anomaly",
    marker_col: str | None = None,
) -> go.Figure:
    """Multi-series time-series line chart with optional anomaly markers."""
    cols = [y] if isinstance(y, str) else y
    fig = go.Figure()
    for i, col in enumerate(cols):
        fig.add_trace(go.Scatter(
            x=data[x], y=data[col], name=col.replace("_", " ").title(),
            line=dict(width=1.8, color=CHART_COLORS[i % len(CHART_COLORS)]),
            mode="lines",
        ))
    if markers is not None and not markers.empty:
        mcol = marker_col or cols[0]
        fig.add_trace(go.Scatter(
            x=markers[x], y=markers[mcol], name=marker_label,
            mode="markers",
            marker=dict(color=RED, size=7, symbol="diamond"),
        ))
    return _chart_layout(fig, title=title, height=height)


def area_stack(
    data: pd.DataFrame,
    x: str,
    y_cols: list[str],
    title: str = "",
    height: int = 340,
) -> go.Figure:
    """Stacked area chart for composition views."""
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        base_color = CHART_COLORS[i % len(CHART_COLORS)]
        fill = _hex_to_rgba(base_color, 0.25)
        fig.add_trace(go.Scatter(
            x=data[x], y=data[col],
            name=col.replace("_", " ").title(),
            stackgroup="one",
            line=dict(width=0.5, color=base_color),
            fillcolor=fill,
        ))
    return _chart_layout(fig, title=title, height=height)


def scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "",
    height: int = 340,
) -> go.Figure:
    """Styled scatter plot."""
    fig = px.scatter(
        data, x=x, y=y, color=color, title=title, opacity=0.5,
        color_continuous_scale=[[0, CYAN], [0.5, GREEN], [1, ORANGE]],
    )
    fig.update_traces(marker=dict(size=4))
    return _chart_layout(fig, title="", height=height)


def bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "",
    height: int = 340,
    horizontal: bool = False,
) -> go.Figure:
    """Styled bar chart."""
    orientation = "h" if horizontal else "v"
    fig = px.bar(
        data, x=x if not horizontal else y, y=y if not horizontal else x,
        color=color, title=title, orientation=orientation,
    )
    return _chart_layout(fig, title="", height=height)


def gauge(
    value: float,
    title: str = "",
    min_val: float = 0,
    max_val: float = 100,
    thresholds: list[tuple[float, str]] | None = None,
    suffix: str = "",
    height: int = 220,
) -> go.Figure:
    """Radial gauge indicator."""
    steps = []
    if thresholds:
        prev = min_val
        for limit, color in thresholds:
            steps.append(dict(range=[prev, limit], color=_hex_to_rgba(color, 0.1)))
            prev = limit
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix=suffix, font=dict(size=32, color=TEXT)),
        title=dict(text=title, font=dict(size=12, color=TEXT_MUTED)),
        gauge=dict(
            axis=dict(range=[min_val, max_val], tickcolor=TEXT_MUTED, tickfont=dict(size=10, color=TEXT_MUTED)),
            bar=dict(color=GREEN, thickness=0.7),
            bgcolor=BG_CARD,
            borderwidth=0,
            steps=steps,
        ),
    ))
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=40, b=10),
    )
    return fig


def sparkline_svg(values: list[float], color: str = GREEN, width: int = 80, height: int = 24) -> str:
    """Generate a minimal SVG sparkline from a list of values."""
    if not values or len(values) < 2:
        return ""
    mn, mx = min(values), max(values)
    rng = mx - mn if mx != mn else 1
    points = []
    for i, v in enumerate(values):
        x = i / (len(values) - 1) * width
        y = height - ((v - mn) / rng) * (height - 2) - 1
        points.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(points)
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg>'
    )


def radar_chart(
    categories: list[str],
    current: list[float],
    scenario: list[float] | None = None,
    title: str = "",
    height: int = 340,
) -> go.Figure:
    """Radar/spider chart for multi-dimensional comparison."""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=current + [current[0]], theta=categories + [categories[0]],
        fill="toself", name="Current",
        line=dict(color=GREEN, width=2),
        fillcolor="rgba(0,212,170,0.1)",
    ))
    if scenario:
        fig.add_trace(go.Scatterpolar(
            r=scenario + [scenario[0]], theta=categories + [categories[0]],
            fill="toself", name="Scenario",
            line=dict(color=CYAN, width=2),
            fillcolor="rgba(0,180,216,0.08)",
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=BORDER, tickfont=dict(size=9, color=TEXT_MUTED)),
            angularaxis=dict(gridcolor=BORDER, tickfont=dict(size=11, color=TEXT_SECONDARY)),
        ),
        title=title, height=height, showlegend=True,
    )
    return fig


def heatmap_strip(
    values: list[float],
    labels: list[str],
    title: str = "",
    low_color: str = GREEN,
    high_color: str = RED,
    height: int = 100,
) -> go.Figure:
    """Horizontal heatmap strip (e.g. 24-hour carbon intensity)."""
    fig = go.Figure(go.Heatmap(
        z=[values], x=labels, y=[""],
        colorscale=[[0, low_color], [1, high_color]],
        showscale=True,
        colorbar=dict(tickfont=dict(size=10, color=TEXT_MUTED), len=0.8),
    ))
    fig.update_layout(
        title=title, height=height,
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=40, b=30),
    )
    return fig


def show(fig: go.Figure, key: str | None = None):
    """Render a Plotly figure in the EcoNexus style."""
    st.plotly_chart(
        fig,
        use_container_width=True,
        theme=None,
        key=key,
        config={"displayModeBar": False, "responsive": True},
    )
