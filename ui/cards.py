"""EcoNexus AI — Reusable card components."""

from __future__ import annotations
import streamlit as st
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, RED, ORANGE, YELLOW, CYAN, severity_color,
)


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
        f'<span class="eco-status {status_class}">{status}</span>' if status else ""
    )
    spark_html = f'<div style="margin-top:0.4rem">{sparkline_svg}</div>' if sparkline_svg else ""
    icon_html = f'<span style="margin-right:0.3rem">{icon}</span>' if icon else ""

    st.markdown(
        f"""<div class="eco-card">
            <div class="eco-label">{icon_html}{label}</div>
            <div class="eco-value">{value}</div>
            {delta_html}
            <div style="margin-top:0.4rem">{status_html}</div>
            {spark_html}
        </div>""",
        unsafe_allow_html=True,
    )


def kpi_card_compact(label: str, value: str, sub: str = "", color: str = TEXT):
    """A smaller metric card for secondary KPIs."""
    sub_html = f'<div style="color:{TEXT_MUTED};font-size:0.75rem;margin-top:0.15rem">{sub}</div>' if sub else ""
    st.markdown(
        f"""<div class="eco-card" style="padding:0.8rem 1rem">
            <div class="eco-label">{label}</div>
            <div class="eco-value-sm" style="color:{color}">{value}</div>
            {sub_html}
        </div>""",
        unsafe_allow_html=True,
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
    border = f"border-color: rgba(0,212,170,0.3);" if selected else ""
    glow = "box-shadow: 0 0 20px rgba(0,212,170,0.06);" if selected else ""
    health_color = GREEN if health >= 90 else YELLOW if health >= 70 else RED
    carbon_color = GREEN if carbon_level == "Low" else YELLOW if carbon_level == "Moderate" else ORANGE
    alert_color = RED if alerts > 2 else ORANGE if alerts > 0 else GREEN

    st.markdown(
        f"""<div class="eco-card" style="{border}{glow}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem">
                <div style="font-weight:700;font-size:0.95rem;color:{TEXT}">{name}</div>
                <span class="eco-status eco-status-{'optimal' if health >= 90 else 'warning' if health >= 70 else 'critical'}">{health}% Health</span>
            </div>
            <div style="display:flex;gap:1rem;flex-wrap:wrap;font-size:0.82rem;color:{TEXT_SECONDARY}">
                <div>PUE <span style="color:{TEXT};font-weight:600">{pue:.2f}</span></div>
                <div>Carbon <span style="color:{carbon_color};font-weight:600">{carbon_level}</span></div>
                <div>Alerts <span style="color:{alert_color};font-weight:600">{alerts}</span></div>
            </div>
        </div>""",
        unsafe_allow_html=True,
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
        f'<div style="margin:0.15rem 0;color:{TEXT_SECONDARY};font-size:0.82rem">• {d}</div>'
        for d in details
    )
    action_html = (
        f'<div style="margin-top:0.6rem;padding:0.5rem 0.7rem;background:rgba(0,180,216,0.06);border-radius:8px;font-size:0.82rem;color:{CYAN}">'
        f'<span style="font-weight:600">Action:</span> {action}</div>'
        if action
        else ""
    )

    st.markdown(
        f"""<div class="eco-incident" style="border-left:3px solid {sev_color}">
            <div class="eco-incident-header">
                <span class="eco-status {status_cls}">{severity}</span>
                <span style="color:{TEXT_MUTED};font-size:0.78rem">{timestamp}</span>
            </div>
            <div style="font-weight:600;font-size:0.95rem;color:{TEXT};margin-bottom:0.4rem">{title}</div>
            {detail_items}
            {action_html}
        </div>""",
        unsafe_allow_html=True,
    )


def insight_card(text: str, level: str = "info"):
    """AI insight strip with colour-coded left border."""
    cls = {"warn": "eco-insight-warn", "crit": "eco-insight-crit"}.get(level, "")
    st.markdown(f'<div class="eco-insight {cls}">{text}</div>', unsafe_allow_html=True)


def alert_strip(severity: str, message: str):
    """Compact alert row for the alert centre."""
    color = severity_color(severity)
    st.markdown(
        f"""<div class="eco-alert-strip">
            <div class="eco-alert-dot" style="background:{color}"></div>
            <span style="color:{color};font-weight:600;font-size:0.75rem;min-width:55px">{severity.upper()}</span>
            <span>{message}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "", icon: str = ""):
    """Styled section header within a page."""
    icon_html = f"{icon} " if icon else ""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="eco-section"><h2>{icon_html}{title}</h2>{sub}</div>',
        unsafe_allow_html=True,
    )


def stat_row(items: list[tuple[str, str, str]]):
    """Render a horizontal row of label/value/unit tuples."""
    cells = "".join(
        f'<div style="flex:1;text-align:center">'
        f'<div class="eco-label">{label}</div>'
        f'<div class="eco-value-sm">{value}</div>'
        f'<div style="color:{TEXT_MUTED};font-size:0.72rem">{unit}</div>'
        f'</div>'
        for label, value, unit in items
    )
    st.markdown(
        f'<div style="display:flex;gap:0.5rem;background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem">{cells}</div>',
        unsafe_allow_html=True,
    )
