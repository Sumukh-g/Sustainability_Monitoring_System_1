import streamlit as st
from components.common import filtered_data, get_config, hero
from src.recommendations import generate_recommendations

st.set_page_config(page_title="Recommendations", page_icon="💡", layout="wide")
hero("Recommendations", "Prioritised actions traceable to selected-period evidence")
d, _ = filtered_data()
_, thresholds = get_config()
recs = generate_recommendations(d, thresholds)
if recs.empty:
    st.success("No configured recommendation condition is active for this selection.")
for _, r in recs.iterrows():
    with st.expander(
        f"{r.priority} · {r.title}",
        expanded=r.priority in ("Immediate", "High Priority"),
    ):
        st.write(
            f"**Triggered by:** {r.triggered_by} · **Severity:** {r.severity} · **Confidence:** {r.confidence:.0%}"
        )
        st.write(
            f"**Evidence:** {r.metric} = {r.current_value} (reference {r.reference_value})"
        )
        st.write(f"**Action:** {r.recommended_action}")
        st.write(f"**Expected benefit:** {r.expected_benefit}")
        st.caption(r.explanation)
