import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from navigation import navigation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Site Analytics - Network Operations",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HEADER / NAVIGATION
# ============================================================

navigation("Site Analytics")


# ============================================================
# PAGE CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PAGE WRAPPER
   ========================================================= */

.site-wrapper {
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

.site-title {
    font-size: 28px;
    font-weight: 700;
    color: #111111;
    margin: 0;
}

.site-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
    margin-bottom: 18px;
}


/* =========================================================
   SITE ANALYTICS PANELS
   ========================================================= */

div[class*="st-key-site_kpi_"],
div[class*="st-key-site_panel_"] {
    border: 1px solid #8f969f !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    box-sizing: border-box !important;
    box-shadow: none !important;
}


/* =========================================================
   REMOVE INTERNAL STREAMLIT BORDER
   ========================================================= */

div[class*="st-key-site_kpi_"]
div[data-testid="stVerticalBlockBorderWrapper"],

div[class*="st-key-site_panel_"]
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    box-shadow: none !important;
}


/* =========================================================
   KPI CONTENT
   ========================================================= */

.site-kpi-title {
    font-size: 12px;
    color: #6b7280;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.site-kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #181818;
    margin-bottom: 6px;
    line-height: 1.15;
}

.site-kpi-good {
    color: #159447;
    font-size: 11px;
    font-weight: 600;
}

.site-kpi-bad {
    color: #d92d20;
    font-size: 11px;
    font-weight: 600;
}

.site-kpi-neutral {
    color: #6b7280;
    font-size: 11px;
    font-weight: 600;
}


/* =========================================================
   PANEL TITLES
   ========================================================= */

.panel-header {
    font-family: Arial, Helvetica, sans-serif;
    margin-bottom: 5px;
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
   SITE STATUS BADGE
   ========================================================= */

.site-status-good {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    background: #eaf8ef;
    color: #15803d;
    font-size: 12px;
    font-weight: 700;
}

.site-status-warning {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    background: #fff7e6;
    color: #b7791f;
    font-size: 12px;
    font-weight: 700;
}

.site-status-bad {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    background: #fdecec;
    color: #c53030;
    font-size: 12px;
    font-weight: 700;
}


/* =========================================================
   METRIC
   ========================================================= */

[data-testid="stMetricValue"] {
    font-size: 23px !important;
    color: #202020 !important;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 4px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

@st.cache_data(ttl=300)
def generate_demo_site_data():

    rng = np.random.default_rng(2026)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=30,
        freq="D"
    )

    sites = [
        "SITE_001",
        "SITE_002",
        "SITE_003",
        "SITE_004",
        "SITE_005",
        "SITE_006"
    ]

    technologies = [
        "2G",
        "3G",
        "4G",
        "5G",
        "VoLTE"
    ]

    rows = []

    for site in sites:

        for technology in technologies:

            for date in dates:

                rows.append({
                    "Date": date,

                    "Site": site,

                    "Technology": technology,

                    "Availability": round(
                        float(
                            rng.uniform(
                                96.5,
                                99.9
                            )
                        ),
                        2
                    ),

                    "CSSR": round(
                        float(
                            rng.uniform(
                                96.0,
                                99.8
                            )
                        ),
                        2
                    ),

                    "DCR": round(
                        float(
                            rng.uniform(
                                0.3,
                                2.8
                            )
                        ),
                        2
                    ),

                    "HOSR": round(
                        float(
                            rng.uniform(
                                94.0,
                                99.5
                            )
                        ),
                        2
                    ),

                    "Traffic": round(
                        float(
                            rng.uniform(
                                150,
                                950
                            )
                        ),
                        1
                    ),

                    "Latency": round(
                        float(
                            rng.uniform(
                                20,
                                55
                            )
                        ),
                        1
                    ),

                    "Active_Users": int(
                        rng.integers(
                            500,
                            6000
                        )
                    ),

                    "Cell":
                        f"{site}_{technology}_CELL_{rng.integers(1,4)}"
                })

    return pd.DataFrame(rows)


@st.cache_data(ttl=300)
def generate_demo_site_alarms():

    rng = np.random.default_rng(3030)

    severities = [
        "Critical",
        "Major",
        "Minor",
        "Warning"
    ]

    alarm_names = [
        "Cell Down",
        "High DCR",
        "Low Availability",
        "Transmission Failure",
        "High Latency",
        "High Congestion",
        "Low HOSR",
        "High Packet Loss"
    ]

    technologies = [
        "2G",
        "3G",
        "4G",
        "5G",
        "VoLTE"
    ]

    sites = [
        "SITE_001",
        "SITE_002",
        "SITE_003",
        "SITE_004",
        "SITE_005",
        "SITE_006"
    ]

    rows = []

    for i in range(25):

        rows.append({
            "Time":
                (
                    pd.Timestamp.now()
                    - pd.Timedelta(
                        minutes=i * 13
                    )
                ).strftime(
                    "%d %b %Y %H:%M"
                ),

            "Site":
                rng.choice(
                    sites
                ),

            "Technology":
                rng.choice(
                    technologies
                ),

            "Severity":
                rng.choice(
                    severities,
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

            "Status":
                rng.choice(
                    [
                        "Open",
                        "Acknowledged",
                        "Resolved"
                    ],
                    p=[
                        0.55,
                        0.30,
                        0.15
                    ]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(
    df,
    possible_names
):

    normalized = {
        str(column).strip().lower():
            column
        for column in df.columns
    }

    for name in possible_names:

        if name.lower() in normalized:

            return normalized[
                name.lower()
            ]

    return None


# ============================================================
# PREPARE UPLOADED KPI DATA
# ============================================================

def prepare_uploaded_data(
    uploaded_df
):

    df = uploaded_df.copy()


    # --------------------------------------------------------
    # DETECT COMMON COLUMN NAMES
    # --------------------------------------------------------

    date_col = find_column(
        df,
        [
            "date",
            "datetime",
            "time",
            "timestamp",
            "day"
        ]
    )

    site_col = find_column(
        df,
        [
            "site",
            "site id",
            "site_id",
            "sitename",
            "site name",
            "node",
            "node name"
        ]
    )

    technology_col = find_column(
        df,
        [
            "technology",
            "tech",
            "rat",
            "network type"
        ]
    )

    cell_col = find_column(
        df,
        [
            "cell",
            "cell name",
            "cell_name",
            "cell id",
            "cell_id"
        ]
    )

    availability_col = find_column(
        df,
        [
            "availability",
            "network availability",
            "availability (%)"
        ]
    )

    cssr_col = find_column(
        df,
        [
            "cssr",
            "cssr (%)",
            "call setup success rate"
        ]
    )

    dcr_col = find_column(
        df,
        [
            "dcr",
            "dcr (%)",
            "dropped call rate",
            "drop call rate"
        ]
    )

    hosr_col = find_column(
        df,
        [
            "hosr",
            "hosr (%)",
            "handover success rate"
        ]
    )

    traffic_col = find_column(
        df,
        [
            "traffic",
            "traffic (gb)",
            "data traffic",
            "tch traffic"
        ]
    )

    latency_col = find_column(
        df,
        [
            "latency",
            "latency (ms)",
            "average latency"
        ]
    )

    users_col = find_column(
        df,
        [
            "active users",
            "active_users",
            "users",
            "subscribers"
        ]
    )


    # --------------------------------------------------------
    # SITE COLUMN IS REQUIRED
    # --------------------------------------------------------

    if site_col is None:

        return None, {
            "reason":
                "No Site column was detected."
        }


    # --------------------------------------------------------
    # BUILD STANDARD DATAFRAME
    # --------------------------------------------------------

    standard = pd.DataFrame()

    standard["Site"] = (
        df[site_col]
        .astype(str)
        .str.strip()
    )


    if date_col is not None:

        standard["Date"] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    else:

        standard["Date"] = (
            pd.Timestamp.today()
        )


    if technology_col is not None:

        standard["Technology"] = (
            df[technology_col]
            .astype(str)
            .str.strip()
        )

    else:

        standard["Technology"] = "Unknown"


    if cell_col is not None:

        standard["Cell"] = (
            df[cell_col]
            .astype(str)
        )

    else:

        standard["Cell"] = (
            standard["Site"]
            + "_CELL"
        )


    metric_mapping = {
        "Availability":
            availability_col,

        "CSSR":
            cssr_col,

        "DCR":
            dcr_col,

        "HOSR":
            hosr_col,

        "Traffic":
            traffic_col,

        "Latency":
            latency_col,

        "Active_Users":
            users_col
    }


    for metric, source_column in metric_mapping.items():

        if source_column is not None:

            standard[metric] = pd.to_numeric(
                df[source_column],
                errors="coerce"
            )

        else:

            standard[metric] = np.nan


    return standard, {
        "reason": None
    }


# ============================================================
# LOAD SITE DATA
# ============================================================

using_uploaded_data = False

source_message = ""


if "kpi_data" in st.session_state:

    uploaded_df = st.session_state[
        "kpi_data"
    ]

    prepared_df, preparation_info = (
        prepare_uploaded_data(
            uploaded_df
        )
    )


    if prepared_df is not None:

        site_df = prepared_df

        using_uploaded_data = True

        source_message = (
            "Using uploaded KPI dataset"
        )

    else:

        site_df = (
            generate_demo_site_data()
        )

        source_message = (
            "Uploaded dataset does not contain "
            "a recognizable Site column. "
            "Demo data is being displayed."
        )

else:

    site_df = (
        generate_demo_site_data()
    )

    source_message = (
        "No KPI dataset is currently loaded. "
        "Demo data is being displayed."
    )


alarms_df = (
    generate_demo_site_alarms()
)


# ============================================================
# CHART HELPERS
# ============================================================

def clean_chart(
    figure,
    height=220,
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
# LINE CHART
# ============================================================

def line_chart(
    df,
    column,
    suffix="",
    height=210
):

    chart_df = (
        df[
            [
                "Date",
                column
            ]
        ]
        .dropna()
        .sort_values(
            "Date"
        )
    )


    figure = go.Figure()


    if not chart_df.empty:

        figure.add_trace(
            go.Scatter(
                x=chart_df["Date"],

                y=chart_df[column],

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
                    + suffix
                    + "<extra></extra>"
                )
            )
        )


    return clean_chart(
        figure,
        height
    )


# ============================================================
# MULTI KPI TREND
# ============================================================

def multi_kpi_chart(
    df
):

    figure = go.Figure()


    metrics = [
        "Availability",
        "CSSR",
        "HOSR"
    ]


    for metric in metrics:

        chart_df = (
            df[
                [
                    "Date",
                    metric
                ]
            ]
            .dropna()
            .sort_values(
                "Date"
            )
        )


        if not chart_df.empty:

            figure.add_trace(
                go.Scatter(
                    x=chart_df["Date"],

                    y=chart_df[metric],

                    mode="lines",

                    name=metric,

                    line=dict(
                        width=2
                    )
                )
            )


    return clean_chart(
        figure,
        height=245,
        legend=True
    )


# ============================================================
# TRAFFIC / USERS CHART
# ============================================================

def traffic_users_chart(
    df
):

    figure = go.Figure()


    chart_df = (
        df
        .sort_values(
            "Date"
        )
    )


    if (
        "Traffic"
        in chart_df.columns
        and
        chart_df["Traffic"].notna().any()
    ):

        figure.add_trace(
            go.Scatter(
                x=chart_df["Date"],

                y=chart_df["Traffic"],

                mode="lines",

                name="Traffic",

                line=dict(
                    width=2
                )
            )
        )


    if (
        "Active_Users"
        in chart_df.columns
        and
        chart_df[
            "Active_Users"
        ].notna().any()
    ):

        figure.add_trace(
            go.Scatter(
                x=chart_df["Date"],

                y=chart_df[
                    "Active_Users"
                ],

                mode="lines",

                name="Active Users",

                line=dict(
                    width=2
                )
            )
        )


    return clean_chart(
        figure,
        height=245,
        legend=True
    )


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
        height=220,
        legend=True
    )


# ============================================================
# PANEL TITLE
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
# KPI CARD
# ============================================================

def site_kpi_card(
    title,
    value,
    note,
    status,
    key
):

    with st.container(
        border=True,
        key=key
    ):

        st.markdown(
            f'<div class="site-kpi-title">'
            f'{title}'
            f'</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            f'<div class="site-kpi-value">'
            f'{value}'
            f'</div>',
            unsafe_allow_html=True
        )


        css_class = (
            "site-kpi-good"
            if status == "good"
            else
            "site-kpi-bad"
            if status == "bad"
            else
            "site-kpi-neutral"
        )


        st.markdown(
            f'<div class="{css_class}">'
            f'{note}'
            f'</div>',
            unsafe_allow_html=True
        )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="site-wrapper">'
    '<div class="site-title">'
    'Site Analytics'
    '</div>'
    '<div class="site-subtitle">'
    'Site-level network performance, cell analysis and alarm monitoring'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA SOURCE MESSAGE
# ============================================================

if using_uploaded_data:

    st.success(
        source_message
    )

else:

    st.info(
        source_message
    )


# ============================================================
# SITE / TECHNOLOGY / PERIOD FILTERS
# ============================================================

sites = sorted(
    site_df[
        "Site"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


if not sites:

    st.error(
        "No valid sites were found in the current dataset."
    )

    st.stop()


filter_site, filter_technology, filter_period, refresh_col = st.columns(
    [
        1.6,
        1.2,
        1.2,
        0.8
    ]
)


with filter_site:

    selected_site = st.selectbox(
        "Site",

        sites,

        key="site_selected_site"
    )


site_subset = site_df[
    site_df["Site"]
    ==
    selected_site
]


technologies = sorted(
    site_subset[
        "Technology"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


with filter_technology:

    technology_options = [
        "All"
    ] + technologies


    selected_technology = st.selectbox(
        "Technology",

        technology_options,

        key="site_selected_technology"
    )


with filter_period:

    selected_period = st.selectbox(
        "Period",

        [
            "Last 24 Hours",
            "Last 7 Days",
            "Last 30 Days"
        ],

        key="site_selected_period"
    )


with refresh_col:

    st.write("")

    refresh = st.button(
        "↻ Refresh",

        use_container_width=True,

        key="site_refresh"
    )


if refresh:

    st.cache_data.clear()

    st.rerun()


# ============================================================
# APPLY TECHNOLOGY FILTER
# ============================================================

filtered_df = site_subset.copy()


if selected_technology != "All":

    filtered_df = filtered_df[
        filtered_df[
            "Technology"
        ]
        ==
        selected_technology
    ]


# ============================================================
# APPLY PERIOD FILTER
# ============================================================

filtered_df["Date"] = pd.to_datetime(
    filtered_df["Date"],
    errors="coerce"
)


filtered_df = filtered_df.dropna(
    subset=[
        "Date"
    ]
)


if not filtered_df.empty:

    max_date = filtered_df[
        "Date"
    ].max()


    if selected_period == "Last 24 Hours":

        start_date = (
            max_date
            -
            pd.Timedelta(
                days=1
            )
        )


    elif selected_period == "Last 7 Days":

        start_date = (
            max_date
            -
            pd.Timedelta(
                days=7
            )
        )


    else:

        start_date = (
            max_date
            -
            pd.Timedelta(
                days=30
            )
        )


    filtered_df = filtered_df[
        filtered_df[
            "Date"
        ]
        >=
        start_date
    ]


# ============================================================
# SAFETY CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No KPI records match the selected filters."
    )

    st.stop()


# ============================================================
# CURRENT SITE METRICS
# ============================================================

latest_df = (
    filtered_df
    .sort_values(
        "Date"
    )
    .tail(
        max(
            1,
            filtered_df[
                "Technology"
            ].nunique()
        )
    )
)


def safe_mean(
    dataframe,
    column
):

    if (
        column
        not in dataframe.columns
        or
        dataframe[column].dropna().empty
    ):

        return np.nan


    return float(
        dataframe[
            column
        ].mean()
    )


availability = safe_mean(
    latest_df,
    "Availability"
)

cssr = safe_mean(
    latest_df,
    "CSSR"
)

dcr = safe_mean(
    latest_df,
    "DCR"
)

hosr = safe_mean(
    latest_df,
    "HOSR"
)

traffic = safe_mean(
    latest_df,
    "Traffic"
)

latency = safe_mean(
    latest_df,
    "Latency"
)


# ============================================================
# SITE STATUS
# ============================================================

if (
    not np.isnan(availability)
    and
    availability >= 98
    and
    (
        np.isnan(dcr)
        or
        dcr <= 2
    )
):

    site_status = "Healthy"

    status_class = (
        "site-status-good"
    )


elif (
    not np.isnan(availability)
    and
    availability >= 95
):

    site_status = "Degraded"

    status_class = (
        "site-status-warning"
    )


else:

    site_status = "Critical"

    status_class = (
        "site-status-bad"
    )


# ============================================================
# SITE HEADER SUMMARY
# ============================================================

with st.container(
    border=True,
    key="site_panel_summary"
):

    summary_left, summary_mid, summary_right = st.columns(
        [
            2.5,
            1.3,
            1.2
        ]
    )


    with summary_left:

        panel_title(
            selected_site,
            (
                "Site operational summary"
                if selected_technology == "All"
                else
                f"{selected_technology} operational summary"
            )
        )


    with summary_mid:

        st.markdown(
            f'<div class="{status_class}">'
            f'{site_status}'
            f'</div>',
            unsafe_allow_html=True
        )


    with summary_right:

        st.metric(
            "Records",
            f"{len(filtered_df):,}"
        )


st.write("")


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5, k6 = st.columns(
    6,
    gap="small"
)


with k1:

    site_kpi_card(
        "Availability",
        (
            f"{availability:.2f}%"
            if not np.isnan(
                availability
            )
            else "—"
        ),
        "Current site availability",
        (
            "good"
            if (
                not np.isnan(
                    availability
                )
                and
                availability >= 98
            )
            else "bad"
        ),
        "site_kpi_availability"
    )


with k2:

    site_kpi_card(
        "CSSR",
        (
            f"{cssr:.2f}%"
            if not np.isnan(
                cssr
            )
            else "—"
        ),
        "Call setup success",
        (
            "good"
            if (
                not np.isnan(cssr)
                and
                cssr >= 97
            )
            else "bad"
        ),
        "site_kpi_cssr"
    )


with k3:

    site_kpi_card(
        "DCR",
        (
            f"{dcr:.2f}%"
            if not np.isnan(
                dcr
            )
            else "—"
        ),
        "Dropped call rate",
        (
            "good"
            if (
                not np.isnan(dcr)
                and
                dcr <= 2
            )
            else "bad"
        ),
        "site_kpi_dcr"
    )


with k4:

    site_kpi_card(
        "HOSR",
        (
            f"{hosr:.2f}%"
            if not np.isnan(
                hosr
            )
            else "—"
        ),
        "Handover success",
        (
            "good"
            if (
                not np.isnan(hosr)
                and
                hosr >= 95
            )
            else "bad"
        ),
        "site_kpi_hosr"
    )


with k5:

    site_kpi_card(
        "Traffic",
        (
            f"{traffic:,.1f}"
            if not np.isnan(
                traffic
            )
            else "—"
        ),
        "Current traffic",
        "neutral",
        "site_kpi_traffic"
    )


with k6:

    site_kpi_card(
        "Latency",
        (
            f"{latency:.1f} ms"
            if not np.isnan(
                latency
            )
            else "—"
        ),
        "Average latency",
        (
            "good"
            if (
                not np.isnan(latency)
                and
                latency <= 40
            )
            else "bad"
        ),
        "site_kpi_latency"
    )


st.write("")


# ============================================================
# MAIN KPI TREND ROW
# ============================================================

performance_col, dcr_col = st.columns(
    [
        1.7,
        1.0
    ],
    gap="small"
)


with performance_col:

    with st.container(
        border=True,
        key="site_panel_kpi_trend"
    ):

        panel_title(
            "Site KPI Performance Trend",
            selected_period
        )


        st.plotly_chart(
            multi_kpi_chart(
                filtered_df
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


with dcr_col:

    with st.container(
        border=True,
        key="site_panel_dcr_trend"
    ):

        panel_title(
            "Dropped Call Rate Trend",
            selected_site
        )


        st.plotly_chart(
            line_chart(
                filtered_df,
                "DCR",
                "%"
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


st.write("")


# ============================================================
# TRAFFIC / LATENCY / TECHNOLOGY
# ============================================================

traffic_col, latency_col, technology_col = st.columns(
    3,
    gap="small"
)


with traffic_col:

    with st.container(
        border=True,
        key="site_panel_traffic"
    ):

        panel_title(
            "Traffic & User Trend",
            "Site utilization"
        )


        st.plotly_chart(
            traffic_users_chart(
                filtered_df
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


with latency_col:

    with st.container(
        border=True,
        key="site_panel_latency"
    ):

        panel_title(
            "Latency Trend",
            "Site network latency"
        )


        st.plotly_chart(
            line_chart(
                filtered_df,
                "Latency",
                " ms"
            ),

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )


with technology_col:

    with st.container(
        border=True,
        key="site_panel_technology"
    ):

        panel_title(
            "Technology Distribution",
            "Records by technology"
        )


        tech_distribution = (
            filtered_df
            .groupby(
                "Technology"
            )
            .size()
            .reset_index(
                name="Count"
            )
        )


        st.plotly_chart(
            donut_chart(
                tech_distribution[
                    "Technology"
                ],

                tech_distribution[
                    "Count"
                ],

                str(
                    tech_distribution[
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
# CELL ANALYSIS
# ============================================================

with st.container(
    border=True,
    key="site_panel_cells"
):

    panel_title(
        "Cell / Sector Analysis",
        "Latest performance records for the selected site"
    )


    cell_columns = [
        "Date",
        "Cell",
        "Technology",
        "Availability",
        "CSSR",
        "DCR",
        "HOSR",
        "Traffic",
        "Latency",
        "Active_Users"
    ]


    cell_columns = [
        column
        for column in cell_columns
        if column in filtered_df.columns
    ]


    latest_cells = (
        filtered_df[
            cell_columns
        ]
        .sort_values(
            "Date",
            ascending=False
        )
        .drop_duplicates(
            subset=[
                "Cell"
            ]
            if "Cell" in cell_columns
            else None
        )
        .head(
            20
        )
    )


    st.dataframe(
        latest_cells,

        use_container_width=True,

        hide_index=True,

        height=330
    )


st.write("")


# ============================================================
# WORST KPI RECORDS
# ============================================================

with st.container(
    border=True,
    key="site_panel_worst"
):

    panel_title(
        "Worst Performing Records",
        "Lowest availability and highest call-drop records"
    )


    worst_records = (
        filtered_df[
            [
                column
                for column in [
                    "Date",
                    "Cell",
                    "Technology",
                    "Availability",
                    "CSSR",
                    "DCR",
                    "HOSR",
                    "Traffic",
                    "Latency"
                ]
                if column
                in filtered_df.columns
            ]
        ]
        .sort_values(
            [
                "Availability",
                "DCR"
            ],
            ascending=[
                True,
                False
            ],
            na_position="last"
        )
        .head(
            10
        )
    )


    st.dataframe(
        worst_records,

        use_container_width=True,

        hide_index=True,

        height=300
    )


st.write("")


# ============================================================
# SITE ALARMS
# ============================================================

site_alarm_df = alarms_df[
    alarms_df[
        "Site"
    ]
    ==
    selected_site
].copy()


if selected_technology != "All":

    site_alarm_df = site_alarm_df[
        site_alarm_df[
            "Technology"
        ]
        ==
        selected_technology
    ]


alarm_summary_col, alarm_table_col = st.columns(
    [
        0.9,
        2.1
    ],
    gap="small"
)


with alarm_summary_col:

    with st.container(
        border=True,
        key="site_panel_alarm_summary"
    ):

        panel_title(
            "Site Alarm Summary",
            "Alarm severity"
        )


        severity_order = [
            "Critical",
            "Major",
            "Minor",
            "Warning"
        ]


        severity_summary = (
            site_alarm_df
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


with alarm_table_col:

    with st.container(
        border=True,
        key="site_panel_alarm_table"
    ):

        panel_title(
            "Site Alarms",
            "Current and recent alarms for the selected site"
        )


        severity_filter_col, status_filter_col, spacer = st.columns(
            [
                1.0,
                1.0,
                2.5
            ]
        )


        with severity_filter_col:

            severity_filter = st.selectbox(
                "Severity",

                [
                    "All",
                    "Critical",
                    "Major",
                    "Minor",
                    "Warning"
                ],

                key="site_alarm_severity"
            )


        with status_filter_col:

            status_filter = st.selectbox(
                "Status",

                [
                    "All",
                    "Open",
                    "Acknowledged",
                    "Resolved"
                ],

                key="site_alarm_status"
            )


        filtered_site_alarms = (
            site_alarm_df.copy()
        )


        if severity_filter != "All":

            filtered_site_alarms = (
                filtered_site_alarms[
                    filtered_site_alarms[
                        "Severity"
                    ]
                    ==
                    severity_filter
                ]
            )


        if status_filter != "All":

            filtered_site_alarms = (
                filtered_site_alarms[
                    filtered_site_alarms[
                        "Status"
                    ]
                    ==
                    status_filter
                ]
            )


        st.dataframe(
            filtered_site_alarms,

            use_container_width=True,

            hide_index=True,

            height=275
        )