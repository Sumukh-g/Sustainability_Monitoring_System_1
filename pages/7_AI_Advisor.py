"""EcoNexus AI — AI Sustainability Advisor."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.layout import page_chrome, global_filters, get_config, empty_state
from ui.cards import kpi_card_compact, section_header
from ui.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SECONDARY, TEXT_MUTED,
    GREEN, CYAN, BLUE, ORANGE, RED, YELLOW, PURPLE,
    severity_color,
)
from src.recommendations import generate_recommendations

# ── Page shell ───────────────────────────────────────────────────────
page_chrome(
    "AI Sustainability Advisor",
    "Prioritised recommendations traceable to operational evidence",
    "💡",
)
data, agg = global_filters()
if data.empty:
    st.stop()

settings, thresholds = get_config()

# ── Predicted peak (best-effort) ─────────────────────────────────────
predicted_peak = None
try:
    from src.forecasting import predict_test

    preds = predict_test(data, "total_energy_kwh")
    predicted_peak = float(preds["predicted"].max())
except Exception:
    pass

# ── Generate recommendations ─────────────────────────────────────────
recs = generate_recommendations(data, thresholds, predicted_peak)

if recs.empty:
    empty_state(
        "✅",
        "No recommendation conditions are active",
        "All monitored metrics are within acceptable thresholds for the selected period.",
    )
    st.stop()

# ── Top metrics strip ────────────────────────────────────────────────
total_recs = len(recs)
high_priority = int((recs["priority"] == "High Priority").sum())
immediate = int((recs["priority"] == "Immediate").sum())

t1, t2, t3 = st.columns(3)
with t1:
    kpi_card_compact("Total Recommendations", str(total_recs), color=CYAN)
with t2:
    kpi_card_compact("High Priority", str(high_priority), color=ORANGE)
with t3:
    kpi_card_compact("Immediate", str(immediate), color=RED)

# ── Section: Priority Matrix ─────────────────────────────────────────
section_header(
    "Priority Matrix",
    "Recommendations positioned by urgency and severity",
    "🎯",
)

priority_order = {"Immediate": 3, "High Priority": 2, "Medium Priority": 1, "Low Priority": 0}
severity_order = {"Critical": 3, "High": 2, "Medium": 1, "Low": 0}

cells = {"tl": [], "tr": [], "bl": [], "br": []}
for _, r in recs.iterrows():
    p_val = priority_order.get(r["priority"], 0)
    s_val = severity_order.get(r["severity"], 0)
    is_high_priority = p_val >= 2
    is_high_severity = s_val >= 2
    if is_high_priority and is_high_severity:
        cells["tr"].append(r)
    elif is_high_priority and not is_high_severity:
        cells["tl"].append(r)
    elif not is_high_priority and is_high_severity:
        cells["br"].append(r)
    else:
        cells["bl"].append(r)


def _matrix_items(items: list, color: str) -> str:
    if not items:
        return f'<div style="color:{TEXT_MUTED};font-size:0.78rem;font-style:italic">None</div>'
    html = ""
    for r in items:
        html += (
            f'<div style="background:rgba({_hex_to_rgb(color)},0.08);border:1px solid rgba({_hex_to_rgb(color)},0.2);'
            f'border-radius:8px;padding:0.5rem 0.7rem;margin-bottom:0.4rem">'
            f'<div style="font-weight:600;font-size:0.85rem;color:{TEXT}">{r["title"]}</div>'
            f'<div style="font-size:0.75rem;color:{TEXT_MUTED};margin-top:0.15rem">{r["triggered_by"]}</div>'
            f"</div>"
        )
    return html


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return ",".join(str(int(h[i : i + 2], 16)) for i in (0, 2, 4))


matrix_html = f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-bottom:1rem">
    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem">
        <div style="font-size:0.7rem;color:{ORANGE};text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:0.6rem">
            ⚡ High Urgency · Low Severity
        </div>
        {_matrix_items(cells["tl"], ORANGE)}
    </div>
    <div style="background:{BG_CARD};border:1px solid rgba(255,51,102,0.2);border-radius:12px;padding:1rem">
        <div style="font-size:0.7rem;color:{RED};text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:0.6rem">
            🔴 High Urgency · High Severity
        </div>
        {_matrix_items(cells["tr"], RED)}
    </div>
    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem">
        <div style="font-size:0.7rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:0.6rem">
            ◽ Low Urgency · Low Severity
        </div>
        {_matrix_items(cells["bl"], TEXT_MUTED)}
    </div>
    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:12px;padding:1rem">
        <div style="font-size:0.7rem;color:{YELLOW};text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:0.6rem">
            ⚠️ Low Urgency · High Severity
        </div>
        {_matrix_items(cells["br"], YELLOW)}
    </div>
</div>
"""
st.html(matrix_html)

# ── Section: Recommendation Cards ────────────────────────────────────
section_header(
    "Recommendation Cards",
    "Detailed action cards with evidence and expected impact",
    "📋",
)

priority_colors = {
    "Immediate": RED,
    "High Priority": ORANGE,
    "Medium Priority": YELLOW,
    "Low Priority": CYAN,
}

for _, r in recs.iterrows():
    p_color = priority_colors.get(r["priority"], TEXT_MUTED)
    confidence_pct = f"{r['confidence']:.0%}" if r["confidence"] <= 1 else f"{r['confidence']:.0f}%"

    card_html = (
        f'<div style="background:{BG_CARD};border:1px solid {BORDER};border-left:4px solid {p_color};'
        f'border-radius:12px;padding:1.15rem 1.25rem;margin-bottom:0.9rem">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.75rem;'
        f'margin-bottom:0.8rem;flex-wrap:wrap">'
        f'<div style="font-size:1.02rem;font-weight:700;color:{TEXT};line-height:1.35">{r["title"]}</div>'
        f'<span style="background:rgba({_hex_to_rgb(p_color)},0.12);color:{p_color};'
        f'padding:0.2rem 0.6rem;border-radius:20px;font-size:0.72rem;font-weight:600;'
        f'letter-spacing:0.05em;text-transform:uppercase;border:1px solid rgba({_hex_to_rgb(p_color)},0.25);'
        f'white-space:nowrap">{r["priority"]}</span></div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0.75rem 1.25rem">'
        f'<div><div style="font-size:0.68rem;color:{TEXT_MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;font-weight:600;margin-bottom:0.2rem">WHY</div>'
        f'<div style="font-size:0.88rem;color:{TEXT_SECONDARY};line-height:1.4">{r["triggered_by"]}</div></div>'
        f'<div><div style="font-size:0.68rem;color:{TEXT_MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;font-weight:600;margin-bottom:0.2rem">CURRENT STATE</div>'
        f'<div style="font-size:0.88rem;color:{TEXT_SECONDARY};line-height:1.4">{r["metric"]} = '
        f'<span style="color:{TEXT};font-weight:600">{r["current_value"]}</span> '
        f'<span style="color:{TEXT_MUTED}">(reference: {r["reference_value"]})</span></div></div>'
        f'<div style="grid-column:1/-1"><div style="font-size:0.68rem;color:{TEXT_MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;font-weight:600;margin-bottom:0.2rem">RECOMMENDED ACTION</div>'
        f'<div style="font-size:0.88rem;color:{CYAN};line-height:1.4">{r["recommended_action"]}</div></div>'
        f'<div><div style="font-size:0.68rem;color:{TEXT_MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;font-weight:600;margin-bottom:0.2rem">EXPECTED IMPACT</div>'
        f'<div style="font-size:0.88rem;color:{GREEN};line-height:1.4">{r["expected_benefit"]}</div></div>'
        f'<div><div style="font-size:0.68rem;color:{TEXT_MUTED};text-transform:uppercase;'
        f'letter-spacing:0.1em;font-weight:600;margin-bottom:0.2rem">CONFIDENCE</div>'
        f'<div style="font-size:0.88rem;color:{TEXT}">{confidence_pct}</div></div></div>'
        f'<div style="margin-top:0.7rem;font-size:0.78rem;color:{TEXT_MUTED};font-style:italic;'
        f'border-top:1px solid {BORDER};padding-top:0.6rem;line-height:1.45">{r["explanation"]}</div></div>'
    )
    st.html(card_html)
