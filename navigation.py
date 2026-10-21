"""Sentinel-inspired shell. Keep existing Streamlit pages and data workflows."""
from datetime import datetime
from html import escape
from pathlib import Path
import streamlit as st
from sentinel_theme import palette

PAGES = [
    ('Overview', '◫  Command centre', 'pages/1_Overview.py'),
    ('KPI Upload', '⇧  Daily KPI upload', 'pages/3_KPI_Upload.py'),
    ('Site Analytics', '⌖  Site analytics', 'pages/4_Site_Analytics.py'),
    ('Report', '▤  Reports & exports', 'pages/5_Report.py'),
    ('Alarms', '⚑  Alerts & alarms', 'pages/6_Alarms.py'),
    ('Settings', '⚙  Settings', 'pages/7_Settings.py'),
    ('Project', '◇  Project case study', 'pages/8_Project.py'),
]
TECHNOLOGIES = ['2G', '3G', '4G', '5G', 'VoLTE']


def initialize_dashboard_settings():
    st.session_state.setdefault('dashboard_theme', 'Dark')
    st.session_state.setdefault('auto_refresh_interval', 'Off')


def get_auto_refresh_seconds():
    return {'Off': None, '30 seconds': 30, '1 minute': 60, '5 minutes': 300,
            '10 minutes': 600, '15 minutes': 900, '30 minutes': 1800}.get(
                st.session_state.get('auto_refresh_interval', 'Off'))


def load_css(current_page='Overview'):
    initialize_dashboard_settings()
    p = palette()
    tokens = ':root{' + ''.join(f'--s-{key}:{value};' for key, value in p.items()) + '}'
    css = (Path(__file__).parent / 'assets' / 'sentinel.css').read_text(encoding='utf-8')
    st.markdown('<style>' + tokens + css + '</style>', unsafe_allow_html=True)


def navigation(current_page='Overview'):
    load_css(current_page)
    with st.sidebar:
        st.markdown('''<div class="sentinel-brand"><span>◈</span><div>NETWORK OPS<small>POWERED BY SENTINEL DESIGN</small></div></div>
        <div class="sentinel-workspace">WORKSPACE<strong>Network performance</strong></div>''', unsafe_allow_html=True)
        for name, label, path in PAGES[:1]:
            _nav_button(name, label, path, current_page)
        st.markdown('<div class="sentinel-section-label">RADIO TECHNOLOGIES</div>', unsafe_allow_html=True)
        with st.expander('⌁  Technology intelligence', expanded=current_page in TECHNOLOGIES):
            for tech in TECHNOLOGIES:
                _nav_button(tech, tech + ' performance', f'pages/technology_{tech}.py', current_page)
        st.markdown('<div class="sentinel-section-label">OPERATIONS</div>', unsafe_allow_html=True)
        for name, label, path in PAGES[1:]:
            _nav_button(name, label, path, current_page)
        st.markdown('''<div class="sentinel-sidebar-footer"><span>●</span> NETWORK INTELLIGENCE<small>Portfolio demonstration<br>Streamlit · SQLite · Plotly</small></div>''', unsafe_allow_html=True)
    st.markdown(
        '<div class="sentinel-topbar"><div>WORKSPACE <span>/ ' + escape(current_page.upper()) + '</span></div>'
        '<div class="sentinel-topbar-right"><b>PORTFOLIO DEMO</b><span>Rendered ' +
        datetime.now().astimezone().strftime('%H:%M:%S %Z') + '</span></div></div>'
        '<div class="sentinel-eyebrow">OBSERVE. UNDERSTAND. RESPOND.</div>',
        unsafe_allow_html=True,
    )


def _nav_button(name, label, path, current_page):
    with st.container(key='sentinel_nav_' + name.replace(' ', '_')):
        if st.button(label, key='sentinel_link_' + name.replace(' ', '_'),
                     type='primary' if current_page == name else 'secondary',
                     use_container_width=True):
            st.switch_page(path)
