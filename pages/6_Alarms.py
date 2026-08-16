import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from navigation import navigation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Alarms - Network Operations",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HEADER / NAVIGATION
# ============================================================

navigation("Alarms")


# ============================================================
# PAGE CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PAGE WRAPPER
   ========================================================= */

.alarms-wrapper {
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

.alarms-title {
    font-size: 28px;
    font-weight: 700;
    color: #111111;
    margin: 0;
}

.alarms-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
    margin-bottom: 18px;
}


/* =========================================================
   ALARM PANELS
   ========================================================= */

div[class*="st-key-alarm_kpi_"],
div[class*="st-key-alarm_panel_"] {
    border: 4px solid #8f969f !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    box-sizing: border-box !important;
    box-shadow: none !important;
}


/* =========================================================
   REMOVE INTERNAL STREAMLIT BORDER
   ========================================================= */

div[class*="st-key-alarm_kpi_"]
div[data-testid="stVerticalBlockBorderWrapper"],

div[class*="st-key-alarm_panel_"]
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    box-shadow: none !important;
}


/* =========================================================
   KPI CONTENT
   ========================================================= */

.alarm-kpi-title {
    font-size: 12px;
    color: #6b7280;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.alarm-kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #181818;
    margin-bottom: 6px;
    line-height: 1.15;
}

.alarm-kpi-note {
    color: #6b7280;
    font-size: 11px;
    font-weight: 600;
}


/* =========================================================
   PANEL TITLE
   ========================================================= */

.panel-header {
    font-family: Arial, Helvetica, sans-serif;
    margin-bottom: 6px;
}

.panel-title {
    color: #202020;
    font-size: 16px;
    font-weight: 700;
}

.panel-subtitle {
    color: #8a8a8a;
    font-size: 11px;
    margin-top: 2px;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 4px;
}


/* =========================================================
   METRIC
   ========================================================= */

[data-testid="stMetricValue"] {
    font-size: 23px !important;
    color: #202020 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
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


def alarm_kpi_card(
    title,
    value,
    note,
    key
):

    with st.container(
        border=True,
        key=key
    ):

        st.markdown(
            f'<div class="alarm-kpi-title">{title}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="alarm-kpi-value">{value}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="alarm-kpi-note">{note}</div>',
            unsafe_allow_html=True
        )


def find_column(
    df,
    possible_names
):

    normalized = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        if name.lower() in normalized:

            return normalized[name.lower()]

    return None


# ============================================================
# DEMO ALARM DATA
# ============================================================

@st.cache_data(ttl=300)
def generate_demo_alarms():

    rng = np.random.default_rng(2026)

    severity_options = [
        "Critical",
        "Major",
        "Minor",
        "Warning"
    ]

    technology_options = [
        "2G",
        "3G",
        "4G",
        "5G",
        "VoLTE"
    ]

    status_options = [
        "Open",
        "Acknowledged",
        "Resolved"
    ]

    alarm_names = [
        "Cell Down",
        "Transmission Failure",
        "High Call Drop Rate",
        "Low CSSR",
        "High Latency",
        "High PRB Utilization",
        "High TCH Congestion",
        "Low HOSR",
        "High Packet Loss",
        "Node Unreachable"
    ]

    sites = [
        "SITE_001",
        "SITE_002",
        "SITE_003",
        "SITE_004",
        "SITE_005",
        "SITE_006",
        "SITE_007"
    ]

    rows = []

    for i in range(60):

        event_time = (
            pd.Timestamp.now()
            - pd.Timedelta(
                minutes=i * 18
            )
        )

        rows.append({
            "Time": event_time,

            "Severity":
                rng.choice(
                    severity_options,
                    p=[
                        0.15,
                        0.30,
                        0.35,
                        0.20
                    ]
                ),

            "Alarm":
                rng.choice(
                    alarm_names
                ),

            "Technology":
                rng.choice(
                    technology_options
                ),

            "Site":
                rng.choice(
                    sites
                ),

            "Status":
                rng.choice(
                    status_options,
                    p=[
                        0.55,
                        0.30,
                        0.15
                    ]
                ),

            "Duration_Minutes":
                int(
                    rng.integers(
                        5,
                        720
                    )
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# TRY TO PREPARE UPLOADED ALARM DATA
# ============================================================

def prepare_uploaded_alarm_data(
    source_df
):

    severity_col = find_column(
        source_df,
        [
            "severity",
            "alarm severity",
            "priority"
        ]
    )

    alarm_col = find_column(
        source_df,
        [
            "alarm",
            "alarm name",
            "alarm description",
            "event"
        ]
    )

    technology_col = find_column(
        source_df,
        [
            "technology",
            "tech",
            "rat",
            "network type"
        ]
    )

    site_col = find_column(
        source_df,
        [
            "site",
            "site id",
            "site_id",
            "site name",
            "sitename",
            "node",
            "node name"
        ]
    )

    status_col = find_column(
        source_df,
        [
            "status",
            "alarm status",
            "state"
        ]
    )

    time_col = find_column(
        source_df,
        [
            "time",
            "date",
            "datetime",
            "timestamp",
            "raised time",
            "event time"
        ]
    )

    duration_col = find_column(
        source_df,
        [
            "duration",
            "duration minutes",
            "duration_minutes",
            "duration (min)"
        ]
    )


    # Alarm + Severity are the minimum useful fields.
    if (
        alarm_col is None
        or
        severity_col is None
    ):

        return None


    prepared = pd.DataFrame()


    prepared["Alarm"] = (
        source_df[
            alarm_col
        ]
        .astype(str)
        .str.strip()
    )


    prepared["Severity"] = (
        source_df[
            severity_col
        ]
        .astype(str)
        .str.strip()
    )


    if technology_col is not None:

        prepared["Technology"] = (
            source_df[
                technology_col
            ]
            .astype(str)
            .str.strip()
        )

    else:

        prepared["Technology"] = "Unknown"


    if site_col is not None:

        prepared["Site"] = (
            source_df[
                site_col
            ]
            .astype(str)
            .str.strip()
        )

    else:

        prepared["Site"] = "Unknown"


    if status_col is not None:

        prepared["Status"] = (
            source_df[
                status_col
            ]
            .astype(str)
            .str.strip()
        )

    else:

        prepared["Status"] = "Open"


    if time_col is not None:

        prepared["Time"] = pd.to_datetime(
            source_df[
                time_col
            ],
            errors="coerce"
        )

    else:

        prepared["Time"] = pd.Timestamp.now()


    if duration_col is not None:

        prepared["Duration_Minutes"] = pd.to_numeric(
            source_df[
                duration_col
            ],
            errors="coerce"
        )

    else:

        prepared["Duration_Minutes"] = np.nan


    return prepared


# ============================================================
# DATA SOURCE
# ============================================================

using_uploaded_alarm_data = False


if "kpi_data" in st.session_state:

    uploaded_df = (
        st.session_state[
            "kpi_data"
        ]
        .copy()
    )

    prepared_alarm_df = (
        prepare_uploaded_alarm_data(
            uploaded_df
        )
    )


    if prepared_alarm_df is not None:

        alarms_df = prepared_alarm_df

        using_uploaded_alarm_data = True

    else:

        alarms_df = (
            generate_demo_alarms()
        )


else:

    alarms_df = (
        generate_demo_alarms()
    )


# ============================================================
# STANDARDIZE VALUES
# ============================================================

alarms_df["Time"] = pd.to_datetime(
    alarms_df["Time"],
    errors="coerce"
)


alarms_df["Severity"] = (
    alarms_df["Severity"]
    .astype(str)
    .str.strip()
    .str.title()
)


alarms_df["Status"] = (
    alarms_df["Status"]
    .astype(str)
    .str.strip()
    .str.title()
)


alarms_df["Technology"] = (
    alarms_df["Technology"]
    .astype(str)
    .str.strip()
)


alarms_df["Site"] = (
    alarms_df["Site"]
    .astype(str)
    .str.strip()
)


# ============================================================
# CHART STYLE
# ============================================================

def clean_chart(
    figure,
    height=230,
    legend=False
):

    figure.update_layout(
        height=height,

        margin=dict(
            l=5,
            r=5,
            t=10,
            b=5
        ),

        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            size=11,
            color="#666666"
        ),

        showlegend=legend,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),

        hoverlabel=dict(
            bgcolor="white"
        )
    )


    figure.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#ededed"
    )


    figure.update_yaxes(
        showgrid=True,
        gridcolor="#f1f1f1",
        zeroline=False
    )


    return figure


# ============================================================
# DONUT CHART
# ============================================================

def donut_chart(
    labels,
    values,
    center_text=""
):

    figure = go.Figure(
        go.Pie(
            labels=labels,
            values=values,

            hole=0.65,

            textinfo="none",

            marker=dict(
                line=dict(
                    color="#ffffff",
                    width=2
                )
            ),

            hovertemplate=(
                "%{label}: %{value}"
                "<extra></extra>"
            )
        )
    )


    if center_text:

        figure.add_annotation(
            text=center_text,
            x=0.5,
            y=0.5,
            showarrow=False,

            font=dict(
                family="Arial",
                size=18,
                color="#222222"
            )
        )


    return clean_chart(
        figure,
        height=230,
        legend=True
    )


# ============================================================
# ALARM TREND CHART
# ============================================================

def alarm_trend_chart(
    df
):

    trend_df = (
        df
        .dropna(
            subset=[
                "Time"
            ]
        )
        .copy()
    )


    if trend_df.empty:

        return clean_chart(
            go.Figure(),
            height=240
        )


    trend_df["Date"] = (
        trend_df["Time"]
        .dt
        .floor("D")
    )


    grouped = (
        trend_df
        .groupby(
            [
                "Date",
                "Severity"
            ]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )


    figure = go.Figure()


    severity_order = [
        "Critical",
        "Major",
        "Minor",
        "Warning"
    ]


    for severity in severity_order:

        severity_df = (
            grouped[
                grouped[
                    "Severity"
                ]
                ==
                severity
            ]
        )


        if not severity_df.empty:

            figure.add_trace(
                go.Scatter(
                    x=severity_df["Date"],
                    y=severity_df["Count"],

                    mode="lines+markers",

                    name=severity,

                    line=dict(
                        width=2
                    ),

                    marker=dict(
                        size=4
                    )
                )
            )


    return clean_chart(
        figure,
        height=240,
        legend=True
    )


# ============================================================
# TECHNOLOGY BAR
# ============================================================

def technology_alarm_chart(
    df
):

    tech_df = (
        df
        .groupby(
            "Technology"
        )
        .size()
        .reset_index(
            name="Count"
        )
        .sort_values(
            "Count",
            ascending=False
        )
    )


    figure = go.Figure(
        go.Bar(
            x=tech_df["Technology"],
            y=tech_df["Count"],

            text=tech_df["Count"],

            textposition="outside"
        )
    )


    return clean_chart(
        figure,
        height=230
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="alarms-wrapper">'
    '<div class="alarms-title">'
    'Network Alarms'
    '</div>'
    '<div class="alarms-subtitle">'
    'Monitor active, acknowledged and historical network alarms'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA SOURCE MESSAGE
# ============================================================

if using_uploaded_alarm_data:

    st.success(
        "Using alarm information from the uploaded dataset."
    )

else:

    st.info(
        "No compatible alarm dataset is currently loaded. "
        "Demo alarm data is being displayed."
    )


# ============================================================
# TOP FILTERS
# ============================================================

filter1, filter2, filter3, filter4, filter5 = st.columns(
    [
        1.0,
        1.0,
        1.1,
        1.3,
        0.8
    ]
)


with filter1:

    severity_filter = st.selectbox(
        "Severity",

        [
            "All",
            "Critical",
            "Major",
            "Minor",
            "Warning"
        ],

        key="alarm_severity_filter"
    )


with filter2:

    status_filter = st.selectbox(
        "Status",

        [
            "All",
            "Open",
            "Acknowledged",
            "Resolved"
        ],

        key="alarm_status_filter"
    )


technology_values = sorted(
    alarms_df[
        "Technology"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


with filter3:

    technology_filter = st.selectbox(
        "Technology",

        [
            "All"
        ]
        +
        technology_values,

        key="alarm_technology_filter"
    )


site_values = sorted(
    alarms_df[
        "Site"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


with filter4:

    site_filter = st.selectbox(
        "Site",

        [
            "All"
        ]
        +
        site_values,

        key="alarm_site_filter"
    )


with filter5:

    st.write("")

    refresh = st.button(
        "↻ Refresh",

        use_container_width=True,

        key="alarm_refresh"
    )


if refresh:

    st.cache_data.clear()

    st.rerun()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = alarms_df.copy()


if severity_filter != "All":

    filtered_df = (
        filtered_df[
            filtered_df[
                "Severity"
            ]
            ==
            severity_filter
        ]
    )


if status_filter != "All":

    filtered_df = (
        filtered_df[
            filtered_df[
                "Status"
            ]
            ==
            status_filter
        ]
    )


if technology_filter != "All":

    filtered_df = (
        filtered_df[
            filtered_df[
                "Technology"
            ]
            ==
            technology_filter
        ]
    )


if site_filter != "All":

    filtered_df = (
        filtered_df[
            filtered_df[
                "Site"
            ]
            ==
            site_filter
        ]
    )


# ============================================================
# KPI COUNTS
# ============================================================

critical_count = int(
    (
        filtered_df[
            "Severity"
        ]
        ==
        "Critical"
    ).sum()
)


major_count = int(
    (
        filtered_df[
            "Severity"
        ]
        ==
        "Major"
    ).sum()
)


minor_count = int(
    (
        filtered_df[
            "Severity"
        ]
        ==
        "Minor"
    ).sum()
)


warning_count = int(
    (
        filtered_df[
            "Severity"
        ]
        ==
        "Warning"
    ).sum()
)


open_count = int(
    (
        filtered_df[
            "Status"
        ]
        ==
        "Open"
    ).sum()
)


total_count = len(
    filtered_df
)


# ============================================================
# KPI ROW
# ============================================================

k1, k2, k3, k4, k5, k6 = st.columns(
    6,
    gap="small"
)


with k1:

    alarm_kpi_card(
        "Critical",
        f"{critical_count:,}",
        "Critical alarms",
        "alarm_kpi_critical"
    )


with k2:

    alarm_kpi_card(
        "Major",
        f"{major_count:,}",
        "Major alarms",
        "alarm_kpi_major"
    )


with k3:

    alarm_kpi_card(
        "Minor",
        f"{minor_count:,}",
        "Minor alarms",
        "alarm_kpi_minor"
    )


with k4:

    alarm_kpi_card(
        "Warning",
        f"{warning_count:,}",
        "Warning alarms",
        "alarm_kpi_warning"
    )


with k5:

    alarm_kpi_card(
        "Open Alarms",
        f"{open_count:,}",
        "Currently open",
        "alarm_kpi_open"
    )


with k6:

    alarm_kpi_card(
        "Total Alarms",
        f"{total_count:,}",
        "Filtered alarms",
        "alarm_kpi_total"
    )


st.write("")


# ============================================================
# SEVERITY SUMMARY + TREND
# ============================================================

severity_col, trend_col = st.columns(
    [
        0.85,
        2.15
    ],
    gap="small"
)


with severity_col:

    with st.container(
        border=True,
        key="alarm_panel_severity"
    ):

        panel_title(
            "Alarm Severity Distribution",
            "Current filtered alarm population"
        )


        severity_order = [
            "Critical",
            "Major",
            "Minor",
            "Warning"
        ]


        severity_summary = (
            filtered_df
            .groupby(
                "Severity"
            )
            .size()
            .reindex(
                severity_order,
                fill_value=0
            )
            .reset_index(
                name="Count"
            )
        )


        st.plotly_chart(
            donut_chart(
                severity_summary[
                    "Severity"
                ],

                severity_summary[
                    "Count"
                ],

                str(
                    severity_summary[
                        "Count"
                    ].sum()
                )
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


with trend_col:

    with st.container(
        border=True,
        key="alarm_panel_trend"
    ):

        panel_title(
            "Alarm Trend",
            "Alarm occurrences over time"
        )


        st.plotly_chart(
            alarm_trend_chart(
                filtered_df
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


st.write("")


# ============================================================
# TECHNOLOGY + STATUS SUMMARY
# ============================================================

technology_col, status_col = st.columns(
    2,
    gap="small"
)


with technology_col:

    with st.container(
        border=True,
        key="alarm_panel_technology"
    ):

        panel_title(
            "Alarms by Technology",
            "Alarm count by network technology"
        )


        st.plotly_chart(
            technology_alarm_chart(
                filtered_df
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


with status_col:

    with st.container(
        border=True,
        key="alarm_panel_status"
    ):

        panel_title(
            "Alarm Status Distribution",
            "Open, acknowledged and resolved alarms"
        )


        status_summary = (
            filtered_df
            .groupby(
                "Status"
            )
            .size()
            .reindex(
                [
                    "Open",
                    "Acknowledged",
                    "Resolved"
                ],
                fill_value=0
            )
            .reset_index(
                name="Count"
            )
        )


        st.plotly_chart(
            donut_chart(
                status_summary[
                    "Status"
                ],

                status_summary[
                    "Count"
                ],

                str(
                    status_summary[
                        "Count"
                    ].sum()
                )
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


st.write("")


# ============================================================
# ACTIVE ALARMS TABLE
# ============================================================

with st.container(
    border=True,
    key="alarm_panel_table"
):

    panel_title(
        "Alarm Details",
        "Filtered network alarm records"
    )


    table_df = (
        filtered_df
        .sort_values(
            "Time",
            ascending=False
        )
        .copy()
    )


    if "Time" in table_df.columns:

        table_df["Time"] = (
            table_df["Time"]
            .dt
            .strftime(
                "%d %b %Y %H:%M"
            )
        )


    st.dataframe(
        table_df,

        use_container_width=True,

        hide_index=True,

        height=420
    )


# ============================================================
# WORST AFFECTED SITES
# ============================================================

st.write("")


with st.container(
    border=True,
    key="alarm_panel_sites"
):

    panel_title(
        "Most Affected Sites",
        "Sites ranked by alarm count"
    )


    site_summary = (
        filtered_df
        .groupby(
            "Site"
        )
        .agg(
            Total_Alarms=(
                "Alarm",
                "size"
            ),

            Critical=(
                "Severity",
                lambda x:
                    (
                        x
                        ==
                        "Critical"
                    )
                    .sum()
            ),

            Major=(
                "Severity",
                lambda x:
                    (
                        x
                        ==
                        "Major"
                    )
                    .sum()
            ),

            Open=(
                "Status",
                lambda x:
                    (
                        x
                        ==
                        "Open"
                    )
                    .sum()
            )
        )
        .reset_index()
        .sort_values(
            "Total_Alarms",
            ascending=False
        )
        .head(
            15
        )
    )


    st.dataframe(
        site_summary,

        use_container_width=True,

        hide_index=True,

        height=330
    )