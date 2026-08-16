import streamlit as st

from navigation import navigation
from technology_dashboard import render_technology_dashboard


st.set_page_config(
    page_title="5G - Network Operations",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


navigation("5G")

render_technology_dashboard("5G")