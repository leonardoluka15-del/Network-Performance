import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Network Performance | Sentinel",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# OPEN OVERVIEW PAGE
st.switch_page("pages/1_Overview.py")