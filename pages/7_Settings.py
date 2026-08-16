import streamlit as st

from navigation import navigation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Settings - Network Operations",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DEFAULT SETTINGS
# ============================================================

if "dashboard_theme" not in st.session_state:
    st.session_state["dashboard_theme"] = "Light"

if "auto_refresh_interval" not in st.session_state:
    st.session_state["auto_refresh_interval"] = "Off"


# ============================================================
# SETTINGS CALLBACKS
# ============================================================

def change_theme():
    """
    Update the dashboard theme immediately when
    the Light/Dark selector changes.
    """

    st.session_state["dashboard_theme"] = (
        st.session_state["settings_theme_selector"]
    )


def change_refresh_interval():
    """
    Update auto-refresh independently from Theme.
    """

    st.session_state["auto_refresh_interval"] = (
        st.session_state["settings_refresh_selector"]
    )


# ============================================================
# HEADER / NAVIGATION
# ============================================================

navigation("Settings")


# ============================================================
# PAGE CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PAGE WRAPPER
   ========================================================= */

.settings-wrapper {
    padding: 22px 26px 8px 26px;
    font-family: Arial, Helvetica, sans-serif;
}


/* =========================================================
   REMOVE EXTRA SPACE BELOW HEADER
   ========================================================= */

.st-key-network_header {
    margin-bottom: 0 !important;
}


div[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
}


/* =========================================================
   PAGE TITLE
   ========================================================= */

.settings-title {
    font-size: 28px;
    font-weight: 700;
    margin: 0;
}


.settings-subtitle {
    font-size: 14px;
    margin-top: 4px;
    margin-bottom: 18px;
}


/* =========================================================
   SETTINGS PANELS
   ========================================================= */

div[class*="st-key-settings_panel_"] {

    border: 4px solid #8f969f !important;

    border-radius: 8px !important;

    box-sizing: border-box !important;

    box-shadow: none !important;
}


/* =========================================================
   REMOVE INTERNAL STREAMLIT BORDER
   ========================================================= */

div[class*="st-key-settings_panel_"]
div[data-testid="stVerticalBlockBorderWrapper"] {

    border: none !important;

    box-shadow: none !important;
}


/* =========================================================
   PANEL TITLE
   ========================================================= */

.panel-header {

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    margin-bottom: 8px;
}


.panel-title {

    font-size: 16px;

    font-weight: 700;
}


.panel-subtitle {

    font-size: 11px;

    margin-top: 2px;
}


/* =========================================================
   CURRENT SETTING TEXT
   ========================================================= */

.settings-current {

    font-size: 13px;

    margin-top: 10px;
}


/* =========================================================
   SETTINGS CONTROL SPACING
   ========================================================= */

.st-key-settings_panel_theme
[data-testid="stRadio"] {

    margin-top: 2px;
}


.st-key-settings_panel_refresh
[data-testid="stSelectbox"] {

    max-width: 420px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER
# ============================================================

def panel_title(
    title,
    subtitle=""
):

    html = (
        f'<div class="panel-header">'
        f'<div class="panel-title">{title}</div>'
        f'<div class="panel-subtitle">{subtitle}</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    (
        '<div class="settings-wrapper">'
        '<div class="settings-title">'
        'Settings'
        '</div>'
        '<div class="settings-subtitle">'
        'Configure dashboard appearance and refresh behaviour'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True
)


# ============================================================
# THEME
# ============================================================

with st.container(
    border=True,
    key="settings_panel_theme"
):

    panel_title(
        "Theme",
        "Choose the dashboard appearance"
    )


    theme_options = [
        "Light",
        "Dark"
    ]


    current_theme = st.session_state.get(
        "dashboard_theme",
        "Light"
    )


    if current_theme not in theme_options:
        current_theme = "Light"


    theme = st.radio(
        "Theme",

        theme_options,

        index=theme_options.index(
            current_theme
        ),

        horizontal=True,

        label_visibility="collapsed",

        key="settings_theme_selector",

        on_change=change_theme
    )


    st.markdown(
        (
            '<div class="settings-current">'
            f'Current theme: <b>{theme}</b>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


# ============================================================
# AUTO REFRESH INTERVAL
# ============================================================

st.write("")


with st.container(
    border=True,
    key="settings_panel_refresh"
):

    panel_title(
        "Auto-Refresh Interval",
        "Choose how often dashboard data should refresh automatically"
    )


    refresh_options = [
        "Off",
        "30 seconds",
        "1 minute",
        "5 minutes",
        "10 minutes",
        "15 minutes",
        "30 minutes"
    ]


    current_refresh = st.session_state.get(
        "auto_refresh_interval",
        "Off"
    )


    if current_refresh not in refresh_options:
        current_refresh = "Off"


    refresh_interval = st.selectbox(
        "Auto-Refresh Interval",

        refresh_options,

        index=refresh_options.index(
            current_refresh
        ),

        label_visibility="collapsed",

        key="settings_refresh_selector",

        on_change=change_refresh_interval
    )


    st.markdown(
        (
            '<div class="settings-current">'
            'Current auto-refresh interval: '
            f'<b>{refresh_interval}</b>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT SETTINGS SUMMARY
# ============================================================

st.write("")


with st.container(
    border=True,
    key="settings_panel_summary"
):

    panel_title(
        "Current Settings",
        "Active dashboard preferences"
    )


    summary_col1, summary_col2 = st.columns(
        2
    )


    with summary_col1:

        st.metric(
            "Theme",
            st.session_state.get(
                "dashboard_theme",
                "Light"
            )
        )


    with summary_col2:

        st.metric(
            "Auto-Refresh",
            st.session_state.get(
                "auto_refresh_interval",
                "Off"
            )
        )