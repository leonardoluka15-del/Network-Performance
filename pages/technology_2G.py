import streamlit as st

from navigation import navigation
from technology_dashboard import render_technology_dashboard


st.set_page_config(
    page_title="2G - Network Operations",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


navigation("2G")

render_technology_dashboard("2G")