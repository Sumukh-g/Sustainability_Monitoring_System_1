"""EcoNexus AI — application entry point with structured navigation."""

import streamlit as st

st.set_page_config(
    page_title="EcoNexus AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

nav = st.navigation(
    {
        "Overview": [
            st.Page(
                "views/command_center.py",
                title="Command Center",
                icon="🌿",
                default=True,
            ),
        ],
        "Operations": [
            st.Page("pages/1_Energy_Intelligence.py", title="Energy Intelligence", icon="⚡"),
            st.Page("pages/2_Water_Intelligence.py", title="Water Intelligence", icon="💧"),
            st.Page("pages/3_Cooling_Intelligence.py", title="Cooling Intelligence", icon="❄️"),
            st.Page("pages/4_Carbon_Intelligence.py", title="Carbon Intelligence", icon="🌍"),
        ],
        "AI & Decision Support": [
            st.Page("pages/5_Forecast_Center.py", title="Forecast Center", icon="📈"),
            st.Page("pages/6_Anomaly_Intelligence.py", title="Anomaly Intelligence", icon="🚨"),
            st.Page("pages/7_AI_Advisor.py", title="AI Advisor", icon="💡"),
            st.Page("pages/8_Scenario_Lab.py", title="Scenario Lab", icon="🧪"),
        ],
        "System": [
            st.Page("pages/9_Model_Intelligence.py", title="Model Intelligence", icon="🧠"),
            st.Page("pages/10_Data_Explorer.py", title="Data Explorer", icon="📂"),
            st.Page("pages/11_System_Health.py", title="System Health", icon="🔧"),
        ],
    },
    position="sidebar",
)
nav.run()
