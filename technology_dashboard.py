import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ============================================================
# TECHNOLOGY CONFIGURATION
# ============================================================

TECH_CONFIG = {

    "2G": {
        "title": "2G Network Performance",
        "subtitle": "GSM network performance, voice quality and capacity monitoring",

        "kpis": [
            ("Availability", "%"),
            ("CSSR", "%"),
            ("DCR", "%"),
            ("HOSR", "%"),
            ("TCH Traffic", " Erl"),
            ("TCH Congestion", "%"),
        ],

        "extra_metric": "SDCCH Congestion",

        "extra_unit": "%",

        "traffic_title": "2G TCH Traffic Trend",

        "quality_title": "2G Voice Quality",

        "quality_metrics": [
            "CSSR",
            "HOSR"
        ]
    },


    "3G": {
        "title": "3G Network Performance",
        "subtitle": "UMTS network accessibility, mobility and traffic performance",

        "kpis": [
            ("Availability", "%"),
            ("CSSR", "%"),
            ("DCR", "%"),
            ("HOSR", "%"),
            ("Data Traffic", " GB"),
            ("RRC Success", "%"),
        ],

        "extra_metric": "RTWP",

        "extra_unit": " dBm",

        "traffic_title": "3G Data Traffic Trend",

        "quality_title": "3G Service Quality",

        "quality_metrics": [
            "CSSR",
            "HOSR",
            "RRC Success"
        ]
    },


    "4G": {
        "title": "4G Network Performance",
        "subtitle": "LTE accessibility, throughput, mobility and capacity monitoring",

        "kpis": [
            ("Availability", "%"),
            ("RRC Success", "%"),
            ("ERAB Success", "%"),
            ("HOSR", "%"),
            ("Data Traffic", " GB"),
            ("PRB Utilization", "%"),
        ],

        "extra_metric": "DL Throughput",

        "extra_unit": " Mbps",

        "traffic_title": "4G Data Traffic Trend",

        "quality_title": "4G Accessibility & Mobility",

        "quality_metrics": [
            "RRC Success",
            "ERAB Success",
            "HOSR"
        ]
    },


    "5G": {
        "title": "5G Network Performance",
        "subtitle": "5G NR accessibility, throughput, utilization and mobility monitoring",

        "kpis": [
            ("Availability", "%"),
            ("RRC Success", "%"),
            ("Session Success", "%"),
            ("HOSR", "%"),
            ("Data Traffic", " GB"),
            ("PRB Utilization", "%"),
        ],

        "extra_metric": "DL Throughput",

        "extra_unit": " Mbps",

        "traffic_title": "5G Data Traffic Trend",

        "quality_title": "5G Accessibility & Mobility",

        "quality_metrics": [
            "RRC Success",
            "Session Success",
            "HOSR"
        ]
    },


    "VoLTE": {
        "title": "VoLTE Performance",
        "subtitle": "Voice over LTE accessibility, retainability and quality monitoring",

        "kpis": [
            ("Availability", "%"),
            ("Call Setup Success", "%"),
            ("Call Drop Rate", "%"),
            ("HOSR", "%"),
            ("Voice Traffic", " Erl"),
            ("SRVCC Success", "%"),
        ],

        "extra_metric": "Packet Loss",

        "extra_unit": "%",

        "traffic_title": "VoLTE Voice Traffic Trend",

        "quality_title": "VoLTE Service Quality",

        "quality_metrics": [
            "Call Setup Success",
            "HOSR",
            "SRVCC Success"
        ]
    }
}


# ============================================================
# CSS
# ============================================================

def load_technology_css():

    st.markdown("""
    <style>

    .technology-wrapper {
        padding: 22px 26px 8px 26px;
        font-family: Arial, Helvetica, sans-serif;
    }

    .st-key-network_header {
        margin-bottom: 0 !important;
    }

    div[data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
    }

    .technology-title {
        font-size: 28px;
        font-weight: 700;
        color: #111111;
        margin: 0;
    }

    .technology-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-top: 4px;
        margin-bottom: 18px;
    }


    /* =====================================================
       TECHNOLOGY CARDS
       ===================================================== */

    div[class*="st-key-tech_kpi_"],
    div[class*="st-key-tech_panel_"] {
        border: 4px solid #8f969f !important;
        border-radius: 8px !important;
        background: #ffffff !important;
        box-sizing: border-box !important;
        box-shadow: none !important;
    }


    div[class*="st-key-tech_kpi_"]
    div[data-testid="stVerticalBlockBorderWrapper"],

    div[class*="st-key-tech_panel_"]
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
        box-shadow: none !important;
    }


    /* =====================================================
       KPI
       ===================================================== */

    .technology-kpi-title {
        font-size: 12px;
        color: #6b7280;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .technology-kpi-value {
        font-size: 26px;
        color: #181818;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .technology-kpi-note {
        font-size: 11px;
        font-weight: 600;
        color: #6b7280;
    }


    /* =====================================================
       PANEL TITLE
       ===================================================== */

    .panel-header {
        font-family: Arial, Helvetica, sans-serif;
        margin-bottom: 5px;
    }

    .panel-title {
        font-size: 16px;
        color: #202020;
        font-weight: 700;
    }

    .panel-subtitle {
        font-size: 11px;
        color: #8a8a8a;
        margin-top: 2px;
    }


    [data-testid="stDataFrame"] {
        border-radius: 4px;
    }

    </style>
    """, unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def panel_title(title, subtitle=""):

    st.markdown(
        (
            f'<div class="panel-header">'
            f'<div class="panel-title">{title}</div>'
            f'<div class="panel-subtitle">{subtitle}</div>'
            f'</div>'
        ),
        unsafe_allow_html=True
    )


def technology_kpi(
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
            f'<div class="technology-kpi-title">{title}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="technology-kpi-value">{value}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="technology-kpi-note">{note}</div>',
            unsafe_allow_html=True
        )


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
# DEMO DATA
# ============================================================

@st.cache_data(ttl=300)
def generate_technology_data(
    technology,
    days=30
):

    seed_map = {
        "2G": 2002,
        "3G": 3003,
        "4G": 4004,
        "5G": 5005,
        "VoLTE": 6006
    }

    rng = np.random.default_rng(
        seed_map[technology]
    )

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=days,
        freq="D"
    )

    df = pd.DataFrame({
        "Date": dates,

        "Availability":
            np.round(
                rng.uniform(
                    96.5,
                    99.9,
                    days
                ),
                2
            ),

        "CSSR":
            np.round(
                rng.uniform(
                    96.0,
                    99.8,
                    days
                ),
                2
            ),

        "DCR":
            np.round(
                rng.uniform(
                    0.4,
                    2.5,
                    days
                ),
                2
            ),

        "HOSR":
            np.round(
                rng.uniform(
                    94.5,
                    99.5,
                    days
                ),
                2
            ),

        "TCH Traffic":
            np.round(
                rng.uniform(
                    5000,
                    12000,
                    days
                ),
                0
            ),

        "TCH Congestion":
            np.round(
                rng.uniform(
                    0.3,
                    4.0,
                    days
                ),
                2
            ),

        "SDCCH Congestion":
            np.round(
                rng.uniform(
                    0.1,
                    2.5,
                    days
                ),
                2
            ),

        "Data Traffic":
            np.round(
                rng.uniform(
                    300,
                    1800,
                    days
                ),
                1
            ),

        "RRC Success":
            np.round(
                rng.uniform(
                    96.5,
                    99.9,
                    days
                ),
                2
            ),

        "ERAB Success":
            np.round(
                rng.uniform(
                    96.0,
                    99.8,
                    days
                ),
                2
            ),

        "Session Success":
            np.round(
                rng.uniform(
                    96.5,
                    99.9,
                    days
                ),
                2
            ),

        "PRB Utilization":
            np.round(
                rng.uniform(
                    25,
                    82,
                    days
                ),
                1
            ),

        "DL Throughput":
            np.round(
                rng.uniform(
                    20,
                    250,
                    days
                ),
                1
            ),

        "RTWP":
            np.round(
                rng.uniform(
                    -108,
                    -85,
                    days
                ),
                1
            ),

        "Call Setup Success":
            np.round(
                rng.uniform(
                    97,
                    99.9,
                    days
                ),
                2
            ),

        "Call Drop Rate":
            np.round(
                rng.uniform(
                    0.1,
                    1.8,
                    days
                ),
                2
            ),

        "Voice Traffic":
            np.round(
                rng.uniform(
                    1800,
                    6500,
                    days
                ),
                0
            ),

        "SRVCC Success":
            np.round(
                rng.uniform(
                    95,
                    99.5,
                    days
                ),
                2
            ),

        "Packet Loss":
            np.round(
                rng.uniform(
                    0.1,
                    2.0,
                    days
                ),
                2
            ),

        "Active Users":
            rng.integers(
                800,
                8500,
                days
            )
    })

    return df


# ============================================================
# WORST CELLS
# ============================================================

@st.cache_data(ttl=300)
def generate_worst_cells(
    technology
):

    rng = np.random.default_rng(
        abs(
            hash(
                technology
            )
        )
        %
        100000
    )

    rows = []

    for index in range(8):

        rows.append({
            "Rank": index + 1,

            "Site":
                f"SITE_{rng.integers(1,999):03d}",

            "Cell":
                f"{technology}_CELL_{rng.integers(100,999)}",

            "Availability (%)":
                round(
                    float(
                        rng.uniform(
                            92,
                            97.5
                        )
                    ),
                    2
                ),

            "DCR (%)":
                round(
                    float(
                        rng.uniform(
                            2,
                            6
                        )
                    ),
                    2
                ),

            "HOSR (%)":
                round(
                    float(
                        rng.uniform(
                            88,
                            96
                        )
                    ),
                    2
                )
        })

    return pd.DataFrame(
        rows
    )


# ============================================================
# ALARMS
# ============================================================

@st.cache_data(ttl=300)
def generate_technology_alarms(
    technology
):

    rng = np.random.default_rng(
        abs(
            hash(
                technology + "_alarm"
            )
        )
        %
        100000
    )

    names = [
        "Cell Down",
        "Transmission Failure",
        "High Congestion",
        "Low Availability",
        "High Drop Rate",
        "Low Handover Success",
        "High Latency",
        "Node Unreachable"
    ]

    rows = []

    for index in range(15):

        rows.append({
            "Time":
                (
                    pd.Timestamp.now()
                    -
                    pd.Timedelta(
                        minutes=index * 18
                    )
                ),

            "Severity":
                rng.choice(
                    [
                        "Critical",
                        "Major",
                        "Minor",
                        "Warning"
                    ]
                ),

            "Site":
                f"SITE_{rng.integers(1,999):03d}",

            "Alarm":
                rng.choice(
                    names
                ),

            "Status":
                rng.choice(
                    [
                        "Open",
                        "Acknowledged",
                        "Resolved"
                    ]
                )
        })

    return pd.DataFrame(
        rows
    )


# ============================================================
# LINE CHART
# ============================================================

def line_chart(
    df,
    column,
    suffix=""
):

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df[column],

            mode="lines+markers",

            line=dict(
                width=2
            ),

            marker=dict(
                size=4
            ),

            hovertemplate=(
                "%{x|%d %b}<br>"
                "%{y:.2f}"
                +
                suffix
                +
                "<extra></extra>"
            )
        )
    )

    return clean_chart(
        figure
    )


# ============================================================
# MULTI CHART
# ============================================================

def multi_chart(
    df,
    metrics
):

    figure = go.Figure()

    for metric in metrics:

        if metric in df.columns:

            figure.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df[metric],

                    mode="lines",

                    name=metric,

                    line=dict(
                        width=2
                    )
                )
            )

    return clean_chart(
        figure,
        height=240,
        legend=True
    )


# ============================================================
# DONUT
# ============================================================

def donut_chart(
    labels,
    values,
    center
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
            )
        )
    )

    figure.add_annotation(
        text=center,
        x=0.5,
        y=0.5,
        showarrow=False,

        font=dict(
            size=18
        )
    )

    return clean_chart(
        figure,
        height=220,
        legend=True
    )


# ============================================================
# TECHNOLOGY DASHBOARD
# ============================================================

def render_technology_dashboard(
    technology
):

    load_technology_css()

    config = TECH_CONFIG[
        technology
    ]

    daily_df = generate_technology_data(
        technology
    )

    worst_cells_df = generate_worst_cells(
        technology
    )

    alarms_df = generate_technology_alarms(
        technology
    )


    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        (
            '<div class="technology-wrapper">'
            f'<div class="technology-title">{config["title"]}</div>'
            f'<div class="technology-subtitle">{config["subtitle"]}</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    # ========================================================
    # PERIOD
    # ========================================================

    spacer, period_col, refresh_col = st.columns(
        [
            5.6,
            1.35,
            1.0
        ]
    )


    with period_col:

        period = st.selectbox(
            "Period",

            [
                "Last 24 Hours",
                "Last 7 Days",
                "Last 30 Days"
            ],

            label_visibility="collapsed",

            key=f"{technology}_period"
        )


    with refresh_col:

        refresh = st.button(
            "↻ Refresh",

            use_container_width=True,

            key=f"{technology}_refresh"
        )


    if refresh:

        st.cache_data.clear()

        st.rerun()


    # ========================================================
    # PERIOD FILTER
    # ========================================================

    if period == "Last 24 Hours":

        display_df = daily_df.tail(
            2
        )

    elif period == "Last 7 Days":

        display_df = daily_df.tail(
            7
        )

    else:

        display_df = daily_df.copy()


    # ========================================================
    # KPI CARDS
    # ========================================================

    columns = st.columns(
        6,
        gap="small"
    )


    for index, (
        metric,
        unit
    ) in enumerate(
        config["kpis"]
    ):

        value = (
            display_df[
                metric
            ]
            .iloc[-1]
        )


        with columns[index]:

            if unit == " Erl":

                display_value = (
                    f"{value:,.0f}{unit}"
                )

            elif unit == " GB":

                display_value = (
                    f"{value:,.1f}{unit}"
                )

            else:

                display_value = (
                    f"{value:.2f}{unit}"
                )


            technology_kpi(
                metric,
                display_value,
                "Current performance",
                f"tech_kpi_{technology}_{index}"
            )


    st.write("")


    # ========================================================
    # PERFORMANCE TRENDS
    # ========================================================

    left, right = st.columns(
        [
            1.4,
            1.0
        ],
        gap="small"
    )


    traffic_metric = (
        "TCH Traffic"
        if technology == "2G"
        else
        "Voice Traffic"
        if technology == "VoLTE"
        else
        "Data Traffic"
    )


    with left:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_traffic"
        ):

            panel_title(
                config[
                    "traffic_title"
                ],
                period
            )

            st.plotly_chart(
                line_chart(
                    display_df,
                    traffic_metric
                ),

                use_container_width=True,

                config={
                    "displayModeBar": False
                }
            )


    with right:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_quality"
        ):

            panel_title(
                config[
                    "quality_title"
                ],
                "Key service quality indicators"
            )

            st.plotly_chart(
                multi_chart(
                    display_df,
                    config[
                        "quality_metrics"
                    ]
                ),

                use_container_width=True,

                config={
                    "displayModeBar": False
                }
            )


    st.write("")


    # ========================================================
    # SECONDARY METRICS
    # ========================================================

    c1, c2, c3 = st.columns(
        3,
        gap="small"
    )


    with c1:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_availability"
        ):

            panel_title(
                "Availability Trend",
                technology
            )

            st.plotly_chart(
                line_chart(
                    display_df,
                    "Availability",
                    "%"
                ),

                use_container_width=True,

                config={
                    "displayModeBar": False
                }
            )


    with c2:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_extra"
        ):

            panel_title(
                config[
                    "extra_metric"
                ],
                "Operational KPI"
            )

            st.plotly_chart(
                line_chart(
                    display_df,
                    config[
                        "extra_metric"
                    ],
                    config[
                        "extra_unit"
                    ]
                ),

                use_container_width=True,

                config={
                    "displayModeBar": False
                }
            )


    with c3:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_users"
        ):

            panel_title(
                "Active Users",
                technology
            )

            st.plotly_chart(
                line_chart(
                    display_df,
                    "Active Users"
                ),

                use_container_width=True,

                config={
                    "displayModeBar": False
                }
            )


    st.write("")


    # ========================================================
    # WORST CELLS
    # ========================================================

    worst_col, alarm_summary_col = st.columns(
        [
            2.0,
            1.0
        ],
        gap="small"
    )


    with worst_col:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_worst"
        ):

            panel_title(
                f"Worst Performing {technology} Cells",
                "Performance degradation ranking"
            )

            st.dataframe(
                worst_cells_df,

                use_container_width=True,

                hide_index=True,

                height=280
            )


    with alarm_summary_col:

        with st.container(
            border=True,
            key=f"tech_panel_{technology}_alarm_summary"
        ):

            panel_title(
                f"{technology} Alarm Summary",
                "Alarm severity"
            )

            alarm_summary = (
                alarms_df
                .groupby(
                    "Severity"
                )
                .size()
                .reset_index(
                    name="Count"
                )
            )

            st.plotly_chart(
                donut_chart(
                    alarm_summary[
                        "Severity"
                    ],

                    alarm_summary[
                        "Count"
                    ],

                    str(
                        alarm_summary[
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


    # ========================================================
    # ALARM TABLE
    # ========================================================

    with st.container(
        border=True,
        key=f"tech_panel_{technology}_alarms"
    ):

        panel_title(
            f"Current {technology} Alarms",
            "Latest technology-specific network alarms"
        )


        severity_col, status_col, blank = (
            st.columns(
                [
                    1.0,
                    1.0,
                    3.0
                ]
            )
        )


        with severity_col:

            severity_filter = st.selectbox(
                "Severity",

                [
                    "All",
                    "Critical",
                    "Major",
                    "Minor",
                    "Warning"
                ],

                key=f"{technology}_severity"
            )


        with status_col:

            status_filter = st.selectbox(
                "Status",

                [
                    "All",
                    "Open",
                    "Acknowledged",
                    "Resolved"
                ],

                key=f"{technology}_status"
            )


        filtered_alarms = (
            alarms_df.copy()
        )


        if severity_filter != "All":

            filtered_alarms = (
                filtered_alarms[
                    filtered_alarms[
                        "Severity"
                    ]
                    ==
                    severity_filter
                ]
            )


        if status_filter != "All":

            filtered_alarms = (
                filtered_alarms[
                    filtered_alarms[
                        "Status"
                    ]
                    ==
                    status_filter
                ]
            )


        filtered_alarms[
            "Time"
        ] = (
            filtered_alarms[
                "Time"
            ]
            .dt
            .strftime(
                "%d %b %Y %H:%M"
            )
        )


        st.dataframe(
            filtered_alarms,

            use_container_width=True,

            hide_index=True,

            height=300
        )