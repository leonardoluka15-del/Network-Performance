import streamlit as st


# ============================================================
# DEFAULT DASHBOARD SETTINGS
# ============================================================

def initialize_dashboard_settings():

    if "dashboard_theme" not in st.session_state:
        st.session_state["dashboard_theme"] = "Light"

    if "auto_refresh_interval" not in st.session_state:
        st.session_state["auto_refresh_interval"] = "Off"


# ============================================================
# AUTO REFRESH HELPER
# ============================================================

def get_auto_refresh_seconds():

    interval = st.session_state.get(
        "auto_refresh_interval",
        "Off"
    )


    refresh_mapping = {

        "Off":
            None,

        "30 seconds":
            30,

        "1 minute":
            60,

        "5 minutes":
            300,

        "10 minutes":
            600,

        "15 minutes":
            900,

        "30 minutes":
            1800

    }


    return refresh_mapping.get(
        interval
    )


# ============================================================
# GLOBAL CSS
# ============================================================

def load_css(
    current_page="Overview"
):

    initialize_dashboard_settings()


    # ========================================================
    # CURRENT THEME
    # ========================================================

    theme = st.session_state.get(
        "dashboard_theme",
        "Light"
    )


    # ========================================================
    # THEME COLORS
    # ========================================================

    if theme == "Dark":

        page_background = "#111827"

        panel_background = "#1f2937"

        text_primary = "#f9fafb"

        text_secondary = "#cbd5e1"

        muted_text = "#94a3b8"

        border_color = "#64748b"

        input_background = "#273449"

        input_text = "#f9fafb"

        button_background = "#273449"

        dataframe_background = "#1f2937"

        dataframe_border = "#64748b"


    else:

        page_background = "#ffffff"

        panel_background = "#ffffff"

        text_primary = "#111111"

        text_secondary = "#666666"

        muted_text = "#8a8a8a"

        border_color = "#8f969f"

        input_background = "#ffffff"

        input_text = "#111111"

        button_background = "#ffffff"

        dataframe_background = "#ffffff"

        dataframe_border = "#d1d5db"


    # ========================================================
    # ACTIVE PAGE CSS
    # ========================================================

    active_css = ""


    page_key_map = {

        "Overview":
            "nav_overview",

        "KPI Upload":
            "nav_upload",

        "Site Analytics":
            "nav_site",

        "Report":
            "nav_report",

        "Alarms":
            "nav_alarms",

        "Settings":
            "nav_settings"

    }


    if current_page in page_key_map:

        active_key = page_key_map[
            current_page
        ]


        active_css += f"""

        .st-key-{active_key} button,
        .st-key-{active_key} button p,
        .st-key-{active_key} button span {{

            color: #ff6258 !important;

        }}

        """


    # ========================================================
    # ACTIVE TECHNOLOGY
    # ========================================================

    if current_page in [
        "2G",
        "3G",
        "4G",
        "5G",
        "VoLTE"
    ]:

        active_css += """

        .st-key-tech_nav
        div[data-baseweb="select"] > div,

        .st-key-tech_nav span {

            color: #ff6258 !important;

        }


        .st-key-tech_nav svg {

            fill: #ff6258 !important;

            color: #ff6258 !important;

        }

        """


    # ========================================================
    # GLOBAL CSS
    # ========================================================

    st.markdown(
        f"""
<style>

/* =========================================================
   MAIN APPLICATION
   ========================================================= */

.stApp {{

    background-color:
        {page_background} !important;

    color:
        {text_primary} !important;

}}


/* =========================================================
   MAIN PAGE CONTAINER
   ========================================================= */

.block-container {{

    padding-top: 0rem !important;

    padding-bottom: 1rem !important;

    padding-left: 0rem !important;

    padding-right: 0rem !important;

    max-width: 100% !important;

}}


div[data-testid="stMainBlockContainer"] {{

    background-color:
        {page_background} !important;

}}


/* =========================================================
   REMOVE STREAMLIT DEFAULT UI
   ========================================================= */

header[data-testid="stHeader"] {{

    display: none !important;

}}


#MainMenu {{

    visibility: hidden !important;

}}


footer {{

    display: none !important;

}}


[data-testid="stSidebar"] {{

    display: none !important;

}}


/* =========================================================
   NETWORK HEADER
   ========================================================= */

.st-key-network_header {{

    background-color:
        #000000 !important;

    height:
        80px !important;

    min-height:
        80px !important;

    padding:
        0 10px !important;

    margin:
        0 !important;

    border-bottom:
        6px solid #ff6258 !important;

    box-sizing:
        border-box !important;

}}


/* =========================================================
   HEADER INTERNAL LAYOUT
   ========================================================= */

.st-key-network_header > div {{

    width:
        100% !important;

}}


.st-key-network_header
div[data-testid="stVerticalBlock"] {{

    gap:
        0 !important;

}}


.st-key-network_header
div[data-testid="stHorizontalBlock"] {{

    gap:
        4px !important;

    align-items:
        center !important;

    height:
        74px !important;

    margin:
        0 !important;

    padding:
        0 !important;

}}


/* =========================================================
   LOGO
   ========================================================= */

.network-logo {{

    height:
        46px;

    width:
        170px;

    border:
        4px solid #ffffff;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    color:
        #ffffff !important;

    background:
        #000000 !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    font-size:
        18px;

    font-weight:
        800;

    white-space:
        nowrap;

    box-sizing:
        border-box;

}}


/* =========================================================
   HEADER NAVIGATION BUTTONS
   ========================================================= */

.st-key-network_header .stButton {{

    margin:
        0 !important;

    padding:
        0 !important;

}}


.st-key-network_header
.stButton > button {{

    background:
        transparent !important;

    color:
        #ffffff !important;

    border:
        none !important;

    border-radius:
        0 !important;

    box-shadow:
        none !important;

    height:
        74px !important;

    min-height:
        74px !important;

    padding:
        0 3px !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        15px !important;

    font-weight:
        600 !important;

    white-space:
        nowrap !important;

}}


.st-key-network_header
.stButton > button p,

.st-key-network_header
.stButton > button span {{

    color:
        #ffffff !important;

}}


/* =========================================================
   HEADER NAVIGATION HOVER
   ========================================================= */

.st-key-network_header
.stButton > button:hover,

.st-key-network_header
.stButton > button:hover p,

.st-key-network_header
.stButton > button:hover span {{

    color:
        #ff6258 !important;

    background:
        transparent !important;

}}


/* =========================================================
   HEADER NAVIGATION FOCUS
   ========================================================= */

.st-key-network_header
.stButton > button:focus,

.st-key-network_header
.stButton > button:focus p,

.st-key-network_header
.stButton > button:focus span {{

    color:
        #ff6258 !important;

    background:
        transparent !important;

    border:
        none !important;

    box-shadow:
        none !important;

}}


/* =========================================================
   TECHNOLOGY DROPDOWN
   ========================================================= */

.st-key-tech_nav {{

    margin:
        0 !important;

    padding:
        0 !important;

}}


.st-key-tech_nav label {{

    display:
        none !important;

}}


.st-key-tech_nav,

.st-key-tech_nav div,

.st-key-tech_nav
div[data-baseweb="select"],

.st-key-tech_nav
div[data-baseweb="select"] > div {{

    background:
        transparent !important;

    background-color:
        transparent !important;

    border:
        none !important;

    box-shadow:
        none !important;

}}


.st-key-tech_nav
div[data-baseweb="select"] > div {{

    color:
        #ffffff !important;

    min-height:
        44px !important;

    padding-left:
        3px !important;

    padding-right:
        3px !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        15px !important;

    font-weight:
        700 !important;

}}


.st-key-tech_nav span,

.st-key-tech_nav input {{

    color:
        #ffffff !important;

}}


.st-key-tech_nav svg {{

    fill:
        #ffffff !important;

    color:
        #ffffff !important;

}}


/* =========================================================
   LOGIN
   ========================================================= */

.network-login {{

    height:
        74px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        flex-end;

    gap:
        7px;

    color:
        #ffffff !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    font-size:
        15px;

    font-weight:
        500;

    white-space:
        nowrap;

}}


.network-login span {{

    color:
        #ffffff !important;

}}


/* =========================================================
   USER ICON
   ========================================================= */

.network-user {{

    width:
        25px;

    height:
        25px;

    position:
        relative;

    flex-shrink:
        0;

}}


.network-user::before {{

    content:
        "";

    position:
        absolute;

    width:
        8px;

    height:
        8px;

    border:
        2px solid #ffffff;

    border-radius:
        50%;

    top:
        0;

    left:
        7px;

}}


.network-user::after {{

    content:
        "";

    position:
        absolute;

    width:
        20px;

    height:
        10px;

    border:
        2px solid #ffffff;

    border-bottom:
        none;

    border-radius:
        14px 14px 0 0;

    bottom:
        0;

    left:
        2px;

}}


/* =========================================================
   GLOBAL PAGE TITLES
   ========================================================= */

.stApp .overview-title,

.stApp .upload-title,

.stApp .site-title,

.stApp .report-title,

.stApp .alarms-title,

.stApp .technology-title,

.stApp .settings-title,

.stApp .dashboard-title {{

    color:
        {text_primary} !important;

}}


/* =========================================================
   GLOBAL PAGE SUBTITLES
   ========================================================= */

.stApp .overview-subtitle,

.stApp .upload-subtitle,

.stApp .site-subtitle,

.stApp .report-subtitle,

.stApp .alarms-subtitle,

.stApp .technology-subtitle,

.stApp .settings-subtitle,

.stApp .dashboard-subtitle {{

    color:
        {text_secondary} !important;

}}


/* =========================================================
   PANEL TITLES
   ========================================================= */

.stApp .panel-title,

.stApp .section-title {{

    color:
        {text_primary} !important;

}}


.stApp .panel-subtitle {{

    color:
        {muted_text} !important;

}}


/* =========================================================
   ALL DASHBOARD KEYED PANELS
   ========================================================= */

.stApp div[class*="st-key-kpi_"],

.stApp div[class*="st-key-panel_"],

.stApp div[class*="st-key-upload_kpi_"],

.stApp div[class*="st-key-upload_panel_"],

.stApp div[class*="st-key-site_kpi_"],

.stApp div[class*="st-key-site_panel_"],

.stApp div[class*="st-key-report_kpi_"],

.stApp div[class*="st-key-report_panel_"],

.stApp div[class*="st-key-alarm_kpi_"],

.stApp div[class*="st-key-alarm_panel_"],

.stApp div[class*="st-key-tech_kpi_"],

.stApp div[class*="st-key-tech_panel_"],

.stApp div[class*="st-key-2g_kpi_"],

.stApp div[class*="st-key-2g_panel_"],

.stApp div[class*="st-key-settings_panel_"] {{

    background-color:
        {panel_background} !important;

    color:
        {text_primary} !important;

    border-color:
        {border_color} !important;

}}


/* =========================================================
   STREAMLIT BORDERED CONTAINERS
   ========================================================= */

.stApp
div[data-testid="stVerticalBlockBorderWrapper"] {{

    background-color:
        {panel_background} !important;

    border-color:
        {border_color} !important;

}}


/* =========================================================
   KPI TITLES
   ========================================================= */

.stApp .kpi-title,

.stApp .upload-kpi-title,

.stApp .site-kpi-title,

.stApp .report-kpi-title,

.stApp .alarm-kpi-title,

.stApp .technology-kpi-title,

.stApp .kpi-label {{

    color:
        {text_secondary} !important;

}}


/* =========================================================
   KPI VALUES
   ========================================================= */

.stApp .kpi-value,

.stApp .upload-kpi-value,

.stApp .site-kpi-value,

.stApp .report-kpi-value,

.stApp .alarm-kpi-value,

.stApp .technology-kpi-value {{

    color:
        {text_primary} !important;

}}


/* =========================================================
   KPI NOTES
   ========================================================= */

.stApp .report-kpi-note,

.stApp .alarm-kpi-note,

.stApp .technology-kpi-note,

.stApp .site-kpi-neutral,

.stApp .settings-current {{

    color:
        {text_secondary} !important;

}}


/* =========================================================
   KPI DELTAS
   ========================================================= */

.stApp .kpi-delta-positive {{

    color:
        #22c55e !important;

}}


.stApp .kpi-delta-negative {{

    color:
        #ff6258 !important;

}}


/* =========================================================
   CLASSIC CARDS
   ========================================================= */

.stApp .kpi-card,

.stApp .dashboard-section {{

    background-color:
        {panel_background} !important;

    border-color:
        {border_color} !important;

    color:
        {text_primary} !important;

}}


/* =========================================================
   STREAMLIT METRICS
   ========================================================= */

.stApp
[data-testid="stMetricLabel"] {{

    color:
        {text_secondary} !important;

}}


.stApp
[data-testid="stMetricLabel"] p {{

    color:
        {text_secondary} !important;

}}


.stApp
[data-testid="stMetricValue"] {{

    color:
        {text_primary} !important;

}}


.stApp
[data-testid="stMetricValue"] > div {{

    color:
        {text_primary} !important;

}}


/* =========================================================
   MARKDOWN TEXT
   ========================================================= */

.stApp
[data-testid="stMarkdownContainer"] {{

    color:
        {text_primary};

}}


.stApp
[data-testid="stMarkdownContainer"] p {{

    color:
        inherit;

}}


/* =========================================================
   SELECTBOX
   ========================================================= */

.stApp
div[data-baseweb="select"] > div {{

    background-color:
        {input_background} !important;

    color:
        {input_text} !important;

    border-color:
        {border_color} !important;

}}


.stApp
div[data-baseweb="select"] span {{

    color:
        {input_text};

}}


/* =========================================================
   TEXT INPUT
   ========================================================= */

.stApp
[data-testid="stTextInput"] input,

.stApp
[data-testid="stNumberInput"] input {{

    background-color:
        {input_background} !important;

    color:
        {input_text} !important;

    border-color:
        {border_color} !important;

}}


/* =========================================================
   RADIO
   ========================================================= */

.stApp
[data-testid="stRadio"] label,

.stApp
[data-testid="stRadio"] p {{

    color:
        {text_primary} !important;

}}


/* =========================================================
   CHECKBOX
   ========================================================= */

.stApp
[data-testid="stCheckbox"] label,

.stApp
[data-testid="stCheckbox"] p {{

    color:
        {text_primary} !important;

}}


/* =========================================================
   WIDGET LABELS
   ========================================================= */

.stApp
[data-testid="stWidgetLabel"],

.stApp
[data-testid="stWidgetLabel"] p {{

    color:
        {text_primary} !important;

}}


/* =========================================================
   NORMAL BUTTONS OUTSIDE HEADER
   ========================================================= */

.stApp
.stButton > button {{

    border-color:
        {border_color};

}}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stApp
[data-testid="stDownloadButton"] button {{

    border-color:
        {border_color} !important;

}}


/* =========================================================
   DATAFRAME
   ========================================================= */

.stApp
[data-testid="stDataFrame"] {{

    background-color:
        {dataframe_background} !important;

    border-color:
        {dataframe_border} !important;

}}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

.stApp
[data-testid="stFileUploaderDropzone"] {{

    background-color:
        {panel_background} !important;

    border-color:
        {border_color} !important;

    color:
        {text_primary} !important;

}}


/* =========================================================
   CAPTIONS
   ========================================================= */

.stApp
[data-testid="stCaptionContainer"] {{

    color:
        {text_secondary} !important;

}}


/* =========================================================
   HEADER MUST ALWAYS STAY BLACK
   ========================================================= */

.stApp .st-key-network_header {{

    background:
        #000000 !important;

    color:
        #ffffff !important;

}}


/* =========================================================
   HEADER BUTTONS MUST ALWAYS BE WHITE
   ========================================================= */

.stApp
.st-key-network_header
.stButton > button,

.stApp
.st-key-network_header
.stButton > button p,

.stApp
.st-key-network_header
.stButton > button span {{

    background:
        transparent !important;

    color:
        #ffffff !important;

}}


/* =========================================================
   HEADER BUTTON HOVER
   ========================================================= */

.stApp
.st-key-network_header
.stButton > button:hover,

.stApp
.st-key-network_header
.stButton > button:hover p,

.stApp
.st-key-network_header
.stButton > button:hover span {{

    color:
        #ff6258 !important;

}}


/* =========================================================
   TECHNOLOGY MUST IGNORE BODY SELECTBOX THEME
   ========================================================= */

.stApp .st-key-tech_nav,

.stApp .st-key-tech_nav div,

.stApp .st-key-tech_nav
div[data-baseweb="select"],

.stApp .st-key-tech_nav
div[data-baseweb="select"] > div {{

    background:
        transparent !important;

    background-color:
        transparent !important;

    border:
        none !important;

    box-shadow:
        none !important;

}}


.stApp .st-key-tech_nav
div[data-baseweb="select"] > div,

.stApp .st-key-tech_nav span,

.stApp .st-key-tech_nav input {{

    color:
        #ffffff !important;

}}


.stApp .st-key-tech_nav svg {{

    color:
        #ffffff !important;

    fill:
        #ffffff !important;

}}


/* =========================================================
   LOGIN MUST ALWAYS BE WHITE
   ========================================================= */

.stApp .network-login,

.stApp .network-login span {{

    color:
        #ffffff !important;

}}


/* =========================================================
   LOGO MUST ALWAYS BE WHITE
   ========================================================= */

.stApp .network-logo {{

    color:
        #ffffff !important;

    border-color:
        #ffffff !important;

    background:
        #000000 !important;

}}


/* =========================================================
   ACTIVE NAVIGATION PAGE

   Keep this LAST so active tab overrides white.
   ========================================================= */

{active_css}

</style>
""",
        unsafe_allow_html=True
    )


# ============================================================
# NAVIGATION
# ============================================================

def navigation(
    current_page="Overview"
):

    initialize_dashboard_settings()


    # ========================================================
    # LOAD GLOBAL THEME
    # ========================================================

    load_css(
        current_page
    )


    # ========================================================
    # BLACK HEADER
    # ========================================================

    with st.container(
        key="network_header"
    ):


        # ====================================================
        # HEADER COLUMNS
        # ====================================================

        (
            logo_col,
            overview_col,
            tech_col,
            upload_col,
            site_col,
            report_col,
            alarm_col,
            settings_col,
            login_col

        ) = st.columns(

            [
                1.45,   # Logo
                0.95,   # Overview
                1.40,   # Technology
                1.15,   # KPI Upload
                1.35,   # Site Analytics
                0.75,   # Report
                0.75,   # Alarms
                0.90,   # Settings
                0.85    # Login
            ],

            gap="small"

        )


        # ====================================================
        # LOGO
        # ====================================================

        with logo_col:

            st.markdown(
                '<div class="network-logo">NETWORK OPS</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # OVERVIEW
        # ====================================================

        with overview_col:

            if st.button(
                "OVERVIEW",

                key="nav_overview",

                use_container_width=True
            ):

                st.switch_page(
                    "pages/1_Overview.py"
                )


        # ====================================================
        # TECHNOLOGY
        # ====================================================

        with tech_col:

            technology_choice = st.selectbox(
                "Technology",

                [
                    "TECHNOLOGY",
                    "2G",
                    "3G",
                    "4G",
                    "5G",
                    "VoLTE"
                ],

                key="tech_nav",

                label_visibility="collapsed"
            )


            if technology_choice == "2G":

                st.switch_page(
                    "pages/technology_2g.py"
                )


            elif technology_choice == "3G":

                st.switch_page(
                    "pages/technology_3g.py"
                )


            elif technology_choice == "4G":

                st.switch_page(
                    "pages/technology_4g.py"
                )


            elif technology_choice == "5G":

                st.switch_page(
                    "pages/technology_5g.py"
                )


            elif technology_choice == "VoLTE":

                st.switch_page(
                    "pages/technology_volte.py"
                )


        # ====================================================
        # KPI UPLOAD
        # ====================================================

        with upload_col:

            if st.button(
                "KPI UPLOAD",

                key="nav_upload",

                use_container_width=True
            ):

                st.switch_page(
                    "pages/3_KPI_Upload.py"
                )


        # ====================================================
        # SITE ANALYTICS
        # ====================================================

        with site_col:

            if st.button(
                "SITE ANALYTICS",

                key="nav_site",

                use_container_width=True
            ):

                st.switch_page(
                    "pages/4_Site_Analytics.py"
                )


        # ====================================================
        # REPORT
        # ====================================================

        with report_col:

            if st.button(
                "REPORT",

                key="nav_report",

                use_container_width=True
            ):

                st.switch_page(
                    "pages/5_Report.py"
                )


        # ====================================================
        # ALARMS
        # ====================================================

        with alarm_col:

            if st.button(
                "ALARMS",

                key="nav_alarms",

                use_container_width=True
            ):

                st.switch_page(
                    "pages/6_Alarms.py"
                )


        # ====================================================
        # SETTINGS
        # ====================================================

        with settings_col:

            if st.button(
                "SETTINGS",

                key="nav_settings",

                use_container_width=True
            ):

                st.switch_page(
                    "pages/7_Settings.py"
                )


        # ====================================================
        # LOGIN
        # ====================================================

        with login_col:

            st.markdown(
                '<div class="network-login">'
                '<div class="network-user"></div>'
                '<span>Log in</span>'
                '</div>',
                unsafe_allow_html=True
            )