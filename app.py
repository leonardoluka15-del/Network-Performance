import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Network Operations Network Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# OPEN OVERVIEW PAGE
# ============================================================

st.switch_page("pages/1_Overview.py")