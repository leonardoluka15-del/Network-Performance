import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from navigation import (
    navigation,
    get_auto_refresh_seconds
)

from data.database import (
    database_has_data,
    get_database_summary,
    get_latest_network_summary,
    get_latest_technology_health,
    get_worst_sites,
    get_kpi_data_by_date,
    get_latest_kpi_date,
    get_site_list
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Overview - Network Operations",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# NAVIGATION
# ============================================================

navigation("Overview")


# ============================================================
# THEME
# ============================================================

dashboard_theme = st.session_state.get(
    "dashboard_theme",
    "Light"
)


if dashboard_theme == "Dark":

    PAGE_BG = "#111827"
    PANEL_BG = "#1f2937"
    CARD_BG = "#1f2937"

    TEXT_PRIMARY = "#f9fafb"
    TEXT_SECONDARY = "#cbd5e1"
    TEXT_MUTED = "#94a3b8"

    BORDER = "#64748b"

    CHART_BG = "#1f2937"
    GRID = "#374151"

else:

    PAGE_BG = "#ffffff"
    PANEL_BG = "#ffffff"
    CARD_BG = "#ffffff"

    TEXT_PRIMARY = "#111111"
    TEXT_SECONDARY = "#666666"
    TEXT_MUTED = "#8a8a8a"

    BORDER = "#8f969f"

    CHART_BG = "#ffffff"
    GRID = "#eeeeee"


CORAL = "#ff6258"
GREEN = "#16a34a"
AMBER = "#d97706"
RED = "#dc2626"
BLUE = "#2563eb"


# ============================================================
# PAGE CSS
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   MAIN
   ========================================================= */

.st-key-network_header {{
    margin-bottom: 0 !important;
}}

div[data-testid="stMainBlockContainer"] {{
    padding-top: 0 !important;
}}


/* =========================================================
   PAGE HEADER
   ========================================================= */

.overview-wrapper {{
    padding: 20px 26px 5px 26px;
    font-family: Arial, Helvetica, sans-serif;
}}


.overview-title {{
    font-size: 28px;
    font-weight: 700;
    color: {TEXT_PRIMARY} !important;
    margin: 0;
}}


.overview-subtitle {{
    font-size: 14px;
    color: {TEXT_SECONDARY} !important;
    margin-top: 4px;
    margin-bottom: 5px;
}}


/* =========================================================
   KPI CARDS
   ========================================================= */

div[class*="st-key-overview_kpi_"] {{

    border: 2px solid {BORDER} !important;

    border-radius: 8px !important;

    background-color: {CARD_BG} !important;

    box-sizing: border-box !important;

    box-shadow: none !important;

}}


div[class*="st-key-overview_kpi_"]
div[data-testid="stVerticalBlockBorderWrapper"] {{

    border: none !important;

    box-shadow: none !important;

    background: transparent !important;

}}


.overview-kpi-label {{

    font-size: 11px;

    color: {TEXT_SECONDARY} !important;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.2px;

    margin-bottom: 8px;

}}


.overview-kpi-value {{

    font-size: 27px;

    font-weight: 700;

    line-height: 1.1;

    color: {TEXT_PRIMARY} !important;

    margin-bottom: 7px;

}}


.overview-kpi-note {{

    font-size: 10px;

    font-weight: 600;

    color: {TEXT_MUTED} !important;

}}


/* =========================================================
   PANELS
   ========================================================= */

div[class*="st-key-overview_panel_"] {{

    border: 2px solid {BORDER} !important;

    border-radius: 8px !important;

    background-color: {PANEL_BG} !important;

    box-sizing: border-box !important;

    box-shadow: none !important;

}}


div[class*="st-key-overview_panel_"]
div[data-testid="stVerticalBlockBorderWrapper"] {{

    border: none !important;

    box-shadow: none !important;

    background: transparent !important;

}}


/* =========================================================
   PANEL TITLES
   ========================================================= */

.panel-header {{

    font-family: Arial, Helvetica, sans-serif;

    margin-bottom: 5px;

}}


.panel-title {{

    color: {TEXT_PRIMARY} !important;

    font-size: 16px;

    font-weight: 700;

}}


.panel-subtitle {{

    color: {TEXT_MUTED} !important;

    font-size: 11px;

    margin-top: 2px;

}}


/* =========================================================
   REPORTING BAR
   ========================================================= */

.overview-reporting-info {{

    font-size: 12px;

    color: {TEXT_SECONDARY} !important;

    font-weight: 600;

}}


/* =========================================================
   HEALTH BADGES
   ========================================================= */

.health-good {{

    color: #16a34a;

    font-weight: 700;

}}


.health-watch {{

    color: #d97706;

    font-weight: 700;

}}


.health-critical {{

    color: #dc2626;

    font-weight: 700;

}}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {{

    border-radius: 4px;

}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def panel_title(
    title,
    subtitle=""
):

    st.markdown(
        (
            '<div class="panel-header">'
            f'<div class="panel-title">{title}</div>'
            f'<div class="panel-subtitle">{subtitle}</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


def kpi_card(
    label,
    value,
    note,
    key
):

    with st.container(
        border=True,
        key=key
    ):

        st.markdown(
            (
                '<div class="overview-kpi-label">'
                f'{label}'
                '</div>'
            ),
            unsafe_allow_html=True
        )


        st.markdown(
            (
                '<div class="overview-kpi-value">'
                f'{value}'
                '</div>'
            ),
            unsafe_allow_html=True
        )


        st.markdown(
            (
                '<div class="overview-kpi-note">'
                f'{note}'
                '</div>'
            ),
            unsafe_allow_html=True
        )


def safe_mean(
    dataframe,
    column
):

    if (
        dataframe.empty
        or
        column not in dataframe.columns
    ):

        return np.nan


    values = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )


    if values.dropna().empty:

        return np.nan


    return float(
        values.mean()
    )


def safe_sum(
    dataframe,
    column
):

    if (
        dataframe.empty
        or
        column not in dataframe.columns
    ):

        return np.nan


    values = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )


    if values.dropna().empty:

        return np.nan


    return float(
        values.sum()
    )


def format_percent(
    value
):

    if pd.isna(
        value
    ):

        return "—"


    return f"{value:.2f}%"


def format_data(
    value_mb
):

    if pd.isna(
        value_mb
    ):

        return "—"


    # MB → GB → TB

    value_gb = (
        value_mb
        /
        1024
    )


    if value_gb >= 1024:

        return (
            f"{value_gb / 1024:.2f} TB"
        )


    return f"{value_gb:.2f} GB"


def format_voice(
    value
):

    if pd.isna(
        value
    ):

        return "—"


    if value >= 1_000_000:

        return (
            f"{value / 1_000_000:.2f}M Erl"
        )


    if value >= 1000:

        return (
            f"{value / 1000:.2f}K Erl"
        )


    return f"{value:.0f} Erl"


# ============================================================
# HEALTH LOGIC
# ============================================================

def technology_status(
    availability,
    accessibility
):

    values = [
        value
        for value in [
            availability,
            accessibility
        ]
        if pd.notna(
            value
        )
    ]


    if not values:

        return "No Data"


    minimum = min(
        values
    )


    if minimum >= 98:

        return "Good"


    if minimum >= 95:

        return "Watch"


    return "Critical"


# ============================================================
# PLOTLY BASE STYLE
# ============================================================

def clean_chart(
    figure,
    height=260,
    legend=False
):

    figure.update_layout(

        height=height,

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),

        paper_bgcolor=CHART_BG,

        plot_bgcolor=CHART_BG,

        font=dict(
            family="Arial",
            size=11,
            color=TEXT_SECONDARY
        ),

        hoverlabel=dict(
            bgcolor=CHART_BG,
            font_color=TEXT_PRIMARY
        ),

        showlegend=legend,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )


    figure.update_xaxes(

        showgrid=False,

        zeroline=False,

        linecolor=GRID,

        tickfont=dict(
            color=TEXT_SECONDARY
        )
    )


    figure.update_yaxes(

        showgrid=True,

        gridcolor=GRID,

        zeroline=False,

        tickfont=dict(
            color=TEXT_SECONDARY
        )
    )


    return figure


# ============================================================
# DATABASE CHECK
# ============================================================

if not database_has_data():

    st.markdown(
        (
            '<div class="overview-wrapper">'
            '<div class="overview-title">'
            'Network Operations Overview'
            '</div>'
            '<div class="overview-subtitle">'
            'Network-wide performance monitoring'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    st.warning(
        (
            "The KPI database is empty. "
            "Upload KPI data from the KPI Upload page first."
        )
    )


    st.stop()


# ============================================================
# DATABASE INFORMATION
# ============================================================

database_summary = (
    get_database_summary()
)


latest_date = (
    get_latest_kpi_date()
)


latest_summary = (
    get_latest_network_summary()
)


technology_health = (
    get_latest_technology_health()
)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    (
        '<div class="overview-wrapper">'
        '<div class="overview-title">'
        'Network Operations Overview'
        '</div>'
        '<div class="overview-subtitle">'
        'Network-wide performance, traffic, technology health and operational exceptions'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True
)


# ============================================================
# TOP CONTROL BAR
# ============================================================

control_left, control_period, control_refresh = (
    st.columns(
        [
            5.0,
            1.3,
            0.9
        ]
    )
)


with control_left:

    if latest_date is not None:

        st.markdown(
            (
                '<div class="overview-reporting-info">'
                'Latest KPI Date: '
                f'<b>{latest_date.strftime("%d %b %Y")}</b>'
                ' &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'Sites: <b>{database_summary["total_sites"]:,}</b>'
                ' &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'Records: <b>{database_summary["total_records"]:,}</b>'
                '</div>'
            ),
            unsafe_allow_html=True
        )


with control_period:

    selected_period = st.selectbox(
        "Period",

        [
            "Last 7 Days",
            "Last 14 Days",
            "Last 30 Days",
            "All Data"
        ],

        index=2,

        label_visibility="collapsed",

        key="overview_period"
    )


with control_refresh:

    if st.button(
        "↻ Refresh",
        use_container_width=True,
        key="overview_refresh"
    ):

        st.cache_data.clear()

        st.rerun()


# ============================================================
# DATE RANGE FOR TRENDS
# ============================================================

if latest_date is None:

    trend_df = pd.DataFrame()


else:

    if selected_period == "Last 7 Days":

        start_date = (
            latest_date
            -
            pd.Timedelta(
                days=6
            )
        )


    elif selected_period == "Last 14 Days":

        start_date = (
            latest_date
            -
            pd.Timedelta(
                days=13
            )
        )


    elif selected_period == "Last 30 Days":

        start_date = (
            latest_date
            -
            pd.Timedelta(
                days=29
            )
        )


    else:

        start_date = None


    trend_df = get_kpi_data_by_date(
        start_date=start_date,
        end_date=latest_date
    )


# ============================================================
# TOP KPI VALUES
# ============================================================

network_availability = latest_summary.get(
    "network_availability",
    np.nan
)


total_data_mb = latest_summary.get(
    "total_data_mb",
    np.nan
)


total_voice = latest_summary.get(
    "total_voice_erlang",
    np.nan
)


accessibility = latest_summary.get(
    "accessibility",
    np.nan
)


drop_rate = latest_summary.get(
    "drop_rate",
    np.nan
)


hosr = latest_summary.get(
    "hosr",
    np.nan
)


# ============================================================
# KPI CARDS
# ============================================================

st.write("")


k1, k2, k3, k4, k5, k6 = st.columns(
    6,
    gap="small"
)


with k1:

    kpi_card(
        "Network Availability",
        format_percent(
            network_availability
        ),
        "Cross-technology average",
        "overview_kpi_availability"
    )


with k2:

    kpi_card(
        "Data Traffic",
        format_data(
            total_data_mb
        ),
        "Latest reporting day",
        "overview_kpi_data"
    )


with k3:

    kpi_card(
        "Voice Traffic",
        format_voice(
            total_voice
        ),
        "2G + 3G + VoLTE",
        "overview_kpi_voice"
    )


with k4:

    kpi_card(
        "Accessibility",
        format_percent(
            accessibility
        ),
        "Network accessibility",
        "overview_kpi_accessibility"
    )


with k5:

    kpi_card(
        "Drop Rate",
        format_percent(
            drop_rate
        ),
        "2G + VoLTE average",
        "overview_kpi_drop"
    )


with k6:

    kpi_card(
        "Mobility / HOSR",
        format_percent(
            hosr
        ),
        "Cross-technology mobility",
        "overview_kpi_hosr"
    )


# ============================================================
# TECHNOLOGY HEALTH
# ============================================================

st.write("")


with st.container(
    border=True,
    key="overview_panel_technology_health"
):

    panel_title(
        "Technology Health",
        (
            "Latest performance snapshot across "
            "2G, 3G, 4G, 5G and VoLTE"
        )
    )


    if technology_health.empty:

        st.info(
            "No technology health information is available."
        )


    else:

        health_df = (
            technology_health.copy()
        )


        # ====================================================
        # STATUS
        # ====================================================

        health_df[
            "Status"
        ] = health_df.apply(
            lambda row:
                technology_status(
                    row[
                        "Availability"
                    ],
                    row[
                        "Accessibility"
                    ]
                ),
            axis=1
        )


        # ====================================================
        # FORMAT TABLE
        # ====================================================

        display_health = (
            health_df.copy()
        )


        for column in [
            "Availability",
            "Accessibility",
            "Retainability",
            "Mobility"
        ]:

            display_health[
                column
            ] = display_health[
                column
            ].apply(
                lambda value:
                    (
                        f"{value:.2f}%"
                        if pd.notna(
                            value
                        )
                        else "—"
                    )
            )


        display_health[
            "Traffic"
        ] = display_health[
            "Traffic"
        ].apply(
            lambda value:
                (
                    f"{value:,.1f}"
                    if pd.notna(
                        value
                    )
                    else "—"
                )
        )


        st.dataframe(

            display_health,

            use_container_width=True,

            hide_index=True,

            height=235,

            column_config={

                "Technology":
                    st.column_config.TextColumn(
                        "Technology",
                        width="small"
                    ),

                "Availability":
                    st.column_config.TextColumn(
                        "Availability"
                    ),

                "Accessibility":
                    st.column_config.TextColumn(
                        "Accessibility"
                    ),

                "Retainability":
                    st.column_config.TextColumn(
                        "Retainability"
                    ),

                "Mobility":
                    st.column_config.TextColumn(
                        "Mobility"
                    ),

                "Traffic":
                    st.column_config.TextColumn(
                        "Traffic"
                    ),

                "Status":
                    st.column_config.TextColumn(
                        "Status"
                    )
            }
        )


# ============================================================
# PREPARE DAILY TREND DATA
# ============================================================

daily_trend = pd.DataFrame()


if not trend_df.empty:

    trend_df[
        "time"
    ] = pd.to_datetime(
        trend_df[
            "time"
        ],
        errors="coerce"
    )


    trend_df = trend_df.dropna(
        subset=[
            "time"
        ]
    )


    daily_rows = []


    for date, group in trend_df.groupby(
        trend_df[
            "time"
        ].dt.normalize()
    ):

        availability_values = []


        for column in [
            "availability_2g",
            "availability_3g",
            "availability_4g",
            "availability_5g",
            "availability_volte"
        ]:

            value = safe_mean(
                group,
                column
            )


            if pd.notna(
                value
            ):

                availability_values.append(
                    value
                )


        accessibility_values = []


        for column in [
            "cssr_2g",
            "cssr_3g",
            "rrc_success_4g",
            "rrc_success_5g",
            "cssr_volte"
        ]:

            value = safe_mean(
                group,
                column
            )


            if pd.notna(
                value
            ):

                accessibility_values.append(
                    value
                )


        data_values = []


        for column in [
            "data_2g_mb",
            "data_3g_mb",
            "data_4g_mb",
            "data_5g_mb"
        ]:

            value = safe_sum(
                group,
                column
            )


            if pd.notna(
                value
            ):

                data_values.append(
                    value
                )


        voice_values = []


        for column in [
            "tch_erlang_2g",
            "erlang_3g",
            "voice_traffic_volte_erlang"
        ]:

            value = safe_sum(
                group,
                column
            )


            if pd.notna(
                value
            ):

                voice_values.append(
                    value
                )


        daily_rows.append(
            {

                "Date":
                    date,

                "Availability":
                    (
                        np.mean(
                            availability_values
                        )
                        if availability_values
                        else np.nan
                    ),

                "Accessibility":
                    (
                        np.mean(
                            accessibility_values
                        )
                        if accessibility_values
                        else np.nan
                    ),

                "Data_MB":
                    (
                        np.sum(
                            data_values
                        )
                        if data_values
                        else np.nan
                    ),

                "Voice_Erlang":
                    (
                        np.sum(
                            voice_values
                        )
                        if voice_values
                        else np.nan
                    )
            }
        )


    daily_trend = pd.DataFrame(
        daily_rows
    )


# ============================================================
# PERFORMANCE TREND
# ============================================================

st.write("")


performance_col, traffic_col = st.columns(
    [
        1.25,
        1.0
    ],
    gap="small"
)


with performance_col:

    with st.container(
        border=True,
        key="overview_panel_performance"
    ):

        panel_title(
            "Network Performance Trend",
            selected_period
        )


        figure = go.Figure()


        if not daily_trend.empty:

            figure.add_trace(
                go.Scatter(
                    x=daily_trend[
                        "Date"
                    ],

                    y=daily_trend[
                        "Availability"
                    ],

                    mode="lines+markers",

                    name="Availability",

                    line=dict(
                        color=CORAL,
                        width=2.4
                    ),

                    marker=dict(
                        size=5
                    )
                )
            )


            figure.add_trace(
                go.Scatter(
                    x=daily_trend[
                        "Date"
                    ],

                    y=daily_trend[
                        "Accessibility"
                    ],

                    mode="lines+markers",

                    name="Accessibility",

                    line=dict(
                        color=BLUE,
                        width=2.2
                    ),

                    marker=dict(
                        size=4
                    )
                )
            )


        figure = clean_chart(
            figure,
            height=285,
            legend=True
        )


        figure.update_yaxes(
            ticksuffix="%"
        )


        st.plotly_chart(
            figure,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


# ============================================================
# DATA TRAFFIC TREND
# ============================================================

with traffic_col:

    with st.container(
        border=True,
        key="overview_panel_data_traffic"
    ):

        panel_title(
            "Data Traffic Trend",
            "2G + 3G + 4G + 5G"
        )


        figure = go.Figure()


        if not daily_trend.empty:

            data_gb = (
                daily_trend[
                    "Data_MB"
                ]
                /
                1024
            )


            figure.add_trace(
                go.Bar(

                    x=daily_trend[
                        "Date"
                    ],

                    y=data_gb,

                    name="Data Traffic",

                    marker_color=CORAL,

                    hovertemplate=(
                        "%{x|%d %b %Y}"
                        "<br>"
                        "%{y:,.2f} GB"
                        "<extra></extra>"
                    )
                )
            )


        figure = clean_chart(
            figure,
            height=285
        )


        figure.update_yaxes(
            title_text="GB"
        )


        st.plotly_chart(
            figure,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


# ============================================================
# AVAILABILITY BY TECHNOLOGY
# ============================================================

st.write("")


availability_col, voice_col = st.columns(
    2,
    gap="small"
)


with availability_col:

    with st.container(
        border=True,
        key="overview_panel_availability_technology"
    ):

        panel_title(
            "Availability by Technology",
            "Latest reporting day"
        )


        technologies = [
            "2G",
            "3G",
            "4G",
            "5G",
            "VoLTE"
        ]


        technology_availability = [

            latest_summary.get(
                "availability_2g",
                np.nan
            ),

            latest_summary.get(
                "availability_3g",
                np.nan
            ),

            latest_summary.get(
                "availability_4g",
                np.nan
            ),

            latest_summary.get(
                "availability_5g",
                np.nan
            ),

            latest_summary.get(
                "availability_volte",
                np.nan
            )
        ]


        valid_technology = [
            technology
            for technology, value
            in zip(
                technologies,
                technology_availability
            )
            if pd.notna(
                value
            )
        ]


        valid_values = [
            value
            for value
            in technology_availability
            if pd.notna(
                value
            )
        ]


        figure = go.Figure(
            go.Bar(

                x=valid_technology,

                y=valid_values,

                text=[
                    f"{value:.2f}%"
                    for value in valid_values
                ],

                textposition="outside",

                marker_color=CORAL,

                hovertemplate=(
                    "%{x}<br>"
                    "%{y:.2f}%"
                    "<extra></extra>"
                )
            )
        )


        figure = clean_chart(
            figure,
            height=270
        )


        if valid_values:

            minimum_axis = max(
                85,
                min(
                    valid_values
                )
                -
                2
            )


            figure.update_yaxes(
                range=[
                    minimum_axis,
                    101
                ],
                ticksuffix="%"
            )


        st.plotly_chart(
            figure,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


# ============================================================
# VOICE TRAFFIC TREND
# ============================================================

with voice_col:

    with st.container(
        border=True,
        key="overview_panel_voice"
    ):

        panel_title(
            "Voice Traffic Trend",
            "2G + 3G + VoLTE"
        )


        figure = go.Figure()


        if not daily_trend.empty:

            figure.add_trace(
                go.Scatter(

                    x=daily_trend[
                        "Date"
                    ],

                    y=daily_trend[
                        "Voice_Erlang"
                    ],

                    mode="lines",

                    fill="tozeroy",

                    name="Voice Traffic",

                    line=dict(
                        color=CORAL,
                        width=2.2
                    ),

                    hovertemplate=(
                        "%{x|%d %b %Y}"
                        "<br>"
                        "%{y:,.0f} Erl"
                        "<extra></extra>"
                    )
                )
            )


        figure = clean_chart(
            figure,
            height=270
        )


        figure.update_yaxes(
            title_text="Erlang"
        )


        st.plotly_chart(
            figure,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


# ============================================================
# TECHNOLOGY TRAFFIC CONTRIBUTION
# ============================================================

st.write("")


traffic_share_col, vendor_col = st.columns(
    [
        1.2,
        0.8
    ],
    gap="small"
)


with traffic_share_col:

    with st.container(
        border=True,
        key="overview_panel_technology_traffic"
    ):

        panel_title(
            "Latest Traffic by Technology",
            "Data and voice contribution"
        )


        latest_day_df = get_kpi_data_by_date(
            start_date=latest_date,
            end_date=latest_date
        )


        traffic_summary = pd.DataFrame(
            {

                "Technology": [
                    "2G Data",
                    "3G Data",
                    "4G Data",
                    "5G Data"
                ],

                "Traffic_MB": [

                    safe_sum(
                        latest_day_df,
                        "data_2g_mb"
                    ),

                    safe_sum(
                        latest_day_df,
                        "data_3g_mb"
                    ),

                    safe_sum(
                        latest_day_df,
                        "data_4g_mb"
                    ),

                    safe_sum(
                        latest_day_df,
                        "data_5g_mb"
                    )
                ]
            }
        )


        traffic_summary = (
            traffic_summary
            .dropna(
                subset=[
                    "Traffic_MB"
                ]
            )
        )


        figure = go.Figure(
            go.Pie(

                labels=traffic_summary[
                    "Technology"
                ],

                values=traffic_summary[
                    "Traffic_MB"
                ],

                hole=0.62,

                textinfo="label+percent",

                hovertemplate=(
                    "%{label}"
                    "<br>"
                    "%{value:,.0f} MB"
                    "<br>"
                    "%{percent}"
                    "<extra></extra>"
                )
            )
        )


        figure.update_layout(

            height=280,

            paper_bgcolor=CHART_BG,

            plot_bgcolor=CHART_BG,

            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),

            font=dict(
                family="Arial",
                size=11,
                color=TEXT_SECONDARY
            ),

            showlegend=False
        )


        st.plotly_chart(
            figure,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


# ============================================================
# VENDOR / SITE COVERAGE
# ============================================================

with vendor_col:

    with st.container(
        border=True,
        key="overview_panel_vendor"
    ):

        panel_title(
            "Network Coverage",
            "Latest database footprint"
        )


        site_list = (
            get_site_list()
        )


        vendor_counts = pd.DataFrame()


        if not site_list.empty:

            vendor_counts = (
                site_list[
                    "vendor"
                ]
                .fillna(
                    "Unknown"
                )
                .value_counts()
                .reset_index()
            )


            vendor_counts.columns = [
                "Vendor",
                "Sites"
            ]


        figure = go.Figure()


        if not vendor_counts.empty:

            figure.add_trace(
                go.Bar(

                    x=vendor_counts[
                        "Vendor"
                    ],

                    y=vendor_counts[
                        "Sites"
                    ],

                    text=vendor_counts[
                        "Sites"
                    ],

                    textposition="outside",

                    marker_color=CORAL
                )
            )


        figure = clean_chart(
            figure,
            height=280
        )


        figure.update_yaxes(
            title_text="Sites"
        )


        st.plotly_chart(
            figure,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


# ============================================================
# WORST PERFORMING SITES
# ============================================================

st.write("")


with st.container(
    border=True,
    key="overview_panel_worst_sites"
):

    panel_title(
        "Sites Requiring Attention",
        (
            "Latest-day ranking based on availability, "
            "drop rate and congestion"
        )
    )


    worst_sites = (
        get_worst_sites(
            limit=10
        )
    )


    if worst_sites.empty:

        st.info(
            "No site exception data is available."
        )


    else:

        display_worst = (
            worst_sites.copy()
        )


        display_worst = display_worst.rename(
            columns={

                "ihs_id":
                    "IHS ID",

                "bts_2g":
                    "BTS",

                "vendor":
                    "Vendor",

                "average_availability":
                    "Average Availability",

                "drop_call_rate_2g":
                    "2G Drop Rate",

                "tch_congestion_2g":
                    "TCH Congestion",

                "dcr_volte":
                    "VoLTE Drop Rate",

                "health_score":
                    "Health Score"
            }
        )


        for column in [
            "Average Availability",
            "2G Drop Rate",
            "TCH Congestion",
            "VoLTE Drop Rate",
            "Health Score"
        ]:

            if column in display_worst.columns:

                display_worst[
                    column
                ] = pd.to_numeric(
                    display_worst[
                        column
                    ],
                    errors="coerce"
                ).round(
                    2
                )


        st.dataframe(

            display_worst,

            use_container_width=True,

            hide_index=True,

            height=390,

            column_config={

                "Average Availability":
                    st.column_config.NumberColumn(
                        "Average Availability",
                        format="%.2f%%"
                    ),

                "2G Drop Rate":
                    st.column_config.NumberColumn(
                        "2G Drop Rate",
                        format="%.2f%%"
                    ),

                "TCH Congestion":
                    st.column_config.NumberColumn(
                        "TCH Congestion",
                        format="%.2f%%"
                    ),

                "VoLTE Drop Rate":
                    st.column_config.NumberColumn(
                        "VoLTE Drop Rate",
                        format="%.2f%%"
                    ),

                "Health Score":
                    st.column_config.NumberColumn(
                        "Health Score",
                        format="%.2f"
                    )
            }
        )


# ============================================================
# DATABASE FOOTER SUMMARY
# ============================================================

st.write("")


with st.container(
    border=True,
    key="overview_panel_database_summary"
):

    panel_title(
        "Data Coverage",
        "Current KPI database reporting scope"
    )


    d1, d2, d3, d4, d5 = st.columns(
        5
    )


    with d1:

        st.metric(
            "Records",
            f"{database_summary['total_records']:,}"
        )


    with d2:

        st.metric(
            "Sites",
            f"{database_summary['total_sites']:,}"
        )


    with d3:

        st.metric(
            "Reporting Days",
            f"{database_summary['reporting_days']:,}"
        )


    with d4:

        st.metric(
            "Vendors",
            f"{database_summary['total_vendors']:,}"
        )


    with d5:

        st.metric(
            "Latest Date",
            (
                pd.to_datetime(
                    database_summary[
                        "latest_date"
                    ]
                ).strftime(
                    "%d %b %Y"
                )
                if database_summary[
                    "latest_date"
                ]
                else "—"
            )
        )