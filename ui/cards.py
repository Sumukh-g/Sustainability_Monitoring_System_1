"""EcoNexus AI — Reusable card components."""

from __future__ import annotations
import streamlit as st
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, RED, ORANGE, YELLOW, CYAN, severity_color,
)


def _html(markup: str) -> None:
    """Render HTML without Markdown indent/code-block side effects."""
    st.html(markup)


def kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
    delta_direction: str = "neutral",
    status: str | None = None,
    icon: str = "",
    sparkline_svg: str = "",
):
    """Render a premium KPI card with optional delta, status badge, and sparkline."""
    delta_class = {
        "up": "eco-delta-pos",
        "down": "eco-delta-neg",
    }.get(delta_direction, "eco-delta-neutral")

    status_class = {
        "optimal": "eco-status-optimal",
        "good": "eco-status-good",
        "warning": "eco-status-warning",
        "elevated": "eco-status-elevated",
        "critical": "eco-status-critical",
    }.get((status or "").lower(), "eco-status-good")

    delta_html = f'<div class="eco-delta {delta_class}">{delta}</div>' if delta else ""
    status_html = (
        f'<div style="margin-top:0.45rem"><span class="eco-status {status_class}">{status}</span></div>'
        if status else ""
    )
    spark_html = f'<div style="margin-top:0.45rem;line-height:0">{sparkline_svg}</div>' if sparkline_svg else ""
    icon_html = f'<span style="margin-right:0.3rem">{icon}</span>' if icon else ""

    _html(
        f'<div class="eco-card">'
        f'<div class="eco-label">{icon_html}{label}</div>'
        f'<div class="eco-value">{value}</div>'
        f'{delta_html}{status_html}{spark_html}'
        f'</div>'
    )


def kpi_card_compact(label: str, value: str, sub: str = "", color: str = TEXT):
    """A smaller metric card for secondary KPIs."""
    sub_html = (
        f'<div style="color:{TEXT_MUTED};font-size:0.75rem;margin-top:0.15rem;line-height:1.3">{sub}</div>'
        if sub else ""
    )
    _html(
        f'<div class="eco-card" style="padding:0.85rem 1rem;min-height:5.2rem">'
        f'<div class="eco-label">{label}</div>'
        f'<div class="eco-value-sm" style="color:{color}">{value}</div>'
        f'{sub_html}'
        f'</div>'
    )


def site_card(
    name: str,
    health: int,
    pue: float,
    carbon_level: str,
    alerts: int,
    selected: bool = False,
):
    """Data-centre site status card."""
    border = "border-color: rgba(0,212,170,0.3);" if selected else ""
    glow = "box-shadow: 0 0 20px rgba(0,212,170,0.06);" if selected else ""
    carbon_color = GREEN if carbon_level == "Low" else YELLOW if carbon_level == "Moderate" else ORANGE
    alert_color = RED if alerts > 2 else ORANGE if alerts > 0 else GREEN
    health_cls = "optimal" if health >= 90 else "warning" if health >= 70 else "critical"

    _html(
        f'<div class="eco-card" style="{border}{glow}">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;margin-bottom:0.6rem;flex-wrap:wrap">'
        f'<div style="font-weight:700;font-size:0.95rem;color:{TEXT}">{name}</div>'
        f'<span class="eco-status eco-status-{health_cls}">{health}% Health</span>'
        f'</div>'
        f'<div style="display:flex;gap:1rem;flex-wrap:wrap;font-size:0.82rem;color:{TEXT_SECONDARY}">'
        f'<div>PUE <span style="color:{TEXT};font-weight:600">{pue:.2f}</span></div>'
        f'<div>Carbon <span style="color:{carbon_color};font-weight:600">{carbon_level}</span></div>'
        f'<div>Alerts <span style="color:{alert_color};font-weight:600">{alerts}</span></div>'
        f'</div></div>'
    )


def incident_card(
    severity: str,
    title: str,
    timestamp: str,
    details: list[str],
    action: str = "",
):
    """Anomaly incident card styled by severity."""
    sev_color = severity_color(severity)
    status_cls = {
        "Critical": "eco-status-critical",
        "High": "eco-status-elevated",
        "Medium": "eco-status-warning",
        "Low": "eco-status-good",
    }.get(severity, "eco-status-good")

    detail_items = "".join(
        f'<div style="margin:0.15rem 0;color:{TEXT_SECONDARY};font-size:0.82rem;line-height:1.35">• {d}</div>'
        for d in details
    )
    action_html = (
        f'<div style="margin-top:0.6rem;padding:0.5rem 0.7rem;background:rgba(0,180,216,0.06);'
        f'border-radius:8px;font-size:0.82rem;color:{CYAN};line-height:1.4">'
        f'<span style="font-weight:600">Action:</span> {action}</div>'
        if action else ""
    )

    _html(
        f'<div class="eco-incident" style="border-left:3px solid {sev_color}">'
        f'<div class="eco-incident-header">'
        f'<span class="eco-status {status_cls}">{severity}</span>'
        f'<span style="color:{TEXT_MUTED};font-size:0.78rem">{timestamp}</span>'
        f'</div>'
        f'<div style="font-weight:600;font-size:0.95rem;color:{TEXT};margin-bottom:0.4rem;line-height:1.35">{title}</div>'
        f'{detail_items}{action_html}</div>'
    )


def insight_card(text: str, level: str = "info"):
    """AI insight strip with colour-coded left border."""
    cls = {"warn": "eco-insight-warn", "crit": "eco-insight-crit"}.get(level, "")
    _html(f'<div class="eco-insight {cls}">{text}</div>')


def alert_strip(severity: str, message: str):
    """Compact alert row for the alert centre."""
    color = severity_color(severity)
    _html(
        f'<div class="eco-alert-strip">'
        f'<div class="eco-alert-dot" style="background:{color}"></div>'
        f'<span style="color:{color};font-weight:600;font-size:0.75rem;min-width:4.2rem;flex-shrink:0">{severity.upper()}</span>'
        f'<span style="line-height:1.4">{message}</span>'
        f'</div>'
    )


def section_header(title: str, subtitle: str = "", icon: str = ""):
    """Styled section header within a page."""
    icon_html = f"{icon} " if icon else ""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    _html(f'<div class="eco-section"><h2>{icon_html}{title}</h2>{sub}</div>')


def stat_row(items: list[tuple[str, str, str]]):
    """Render a horizontal row of label/value/unit tuples."""
    cells = "".join(
        f'<div style="flex:1 1 140px;text-align:center;padding:0.35rem 0.25rem;min-width:0">'
        f'<div class="eco-label">{label}</div>'
        f'<div class="eco-value-sm">{value}</div>'
        f'<div style="color:{TEXT_MUTED};font-size:0.72rem;margin-top:0.15rem">{unit}</div>'
        f'</div>'
        for label, value, unit in items
    )
    _html(
        f'<div style="display:flex;flex-wrap:wrap;gap:0.35rem;background:{BG_CARD};'
        f'border:1px solid {BORDER};border-radius:12px;padding:0.85rem 0.6rem">{cells}</div>'
    )
