import streamlit as st
import pandas as pd
import numpy as np

from io import BytesIO

from navigation import navigation

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import (
    TA_LEFT,
    TA_CENTER
)
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.graphics.shapes import (
    Drawing,
    String
)

from reportlab.graphics.charts.linecharts import (
    HorizontalLineChart
)

from reportlab.graphics.charts.barcharts import (
    VerticalBarChart
)

from reportlab.graphics.widgets.markers import (
    makeMarker
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Report - Network Operations",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HEADER / NAVIGATION
# ============================================================

navigation("Report")


# ============================================================
# PAGE CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PAGE WRAPPER
   ========================================================= */

.report-wrapper {
    padding: 22px 26px 8px 26px;
    font-family: Arial, Helvetica, sans-serif;
}


/* =========================================================
   REMOVE EXTRA SPACE
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

.report-title {
    font-size: 28px;
    font-weight: 700;
    color: #111111;
    margin: 0;
}

.report-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
    margin-bottom: 18px;
}


/* =========================================================
   PANELS
   ========================================================= */

div[class*="st-key-report_kpi_"],
div[class*="st-key-report_panel_"] {

    border: 4px solid #8f969f !important;

    border-radius: 8px !important;

    background-color: #ffffff !important;

    box-sizing: border-box !important;

    box-shadow: none !important;
}


/* =========================================================
   REMOVE INTERNAL BORDER
   ========================================================= */

div[class*="st-key-report_kpi_"]
div[data-testid="stVerticalBlockBorderWrapper"],

div[class*="st-key-report_panel_"]
div[data-testid="stVerticalBlockBorderWrapper"] {

    border: none !important;

    box-shadow: none !important;
}


/* =========================================================
   KPI
   ========================================================= */

.report-kpi-title {

    font-size: 12px;

    color: #6b7280;

    font-weight: 700;

    text-transform: uppercase;

    margin-bottom: 8px;
}


.report-kpi-value {

    font-size: 26px;

    font-weight: 700;

    color: #181818;

    margin-bottom: 6px;

    line-height: 1.15;
}


.report-kpi-note {

    color: #6b7280;

    font-size: 11px;

    font-weight: 600;
}


/* =========================================================
   PANEL TITLES
   ========================================================= */

.panel-header {

    font-family:
        Arial,
        Helvetica,
        sans-serif;

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

</style>
""", unsafe_allow_html=True)


# ============================================================
# BASIC HELPERS
# ============================================================

def panel_title(
    title,
    subtitle=""
):

    st.markdown(
        (
            f'<div class="panel-header">'
            f'<div class="panel-title">{title}</div>'
            f'<div class="panel-subtitle">{subtitle}</div>'
            f'</div>'
        ),
        unsafe_allow_html=True
    )


def report_kpi_card(
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
            (
                f'<div class="report-kpi-title">'
                f'{title}'
                f'</div>'
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            (
                f'<div class="report-kpi-value">'
                f'{value}'
                f'</div>'
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            (
                f'<div class="report-kpi-note">'
                f'{note}'
                f'</div>'
            ),
            unsafe_allow_html=True
        )


# ============================================================
# COLUMN DETECTION
# ============================================================

def normalize_column_name(
    value
):

    return (
        str(value)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
        .replace("  ", " ")
    )


def find_column(
    df,
    possible_names
):

    normalized = {

        normalize_column_name(column):
            column

        for column in df.columns
    }

    for name in possible_names:

        normalized_name = (
            normalize_column_name(
                name
            )
        )

        if normalized_name in normalized:

            return normalized[
                normalized_name
            ]

    return None


def safe_numeric_mean(
    df,
    column
):

    if column is None:

        return np.nan

    numeric = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    if numeric.dropna().empty:

        return np.nan

    return float(
        numeric.mean()
    )


def safe_numeric_sum(
    df,
    column
):

    if column is None:

        return np.nan

    numeric = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    if numeric.dropna().empty:

        return np.nan

    return float(
        numeric.sum()
    )


# ============================================================
# STANDARD COLUMN ALIASES
# ============================================================

COLUMN_ALIASES = {

    "Date": [
        "date",
        "datetime",
        "time",
        "timestamp",
        "day"
    ],

    "Site": [
        "site",
        "site id",
        "site_id",
        "site name",
        "sitename",
        "node",
        "node name"
    ],

    "Cell": [
        "cell",
        "cell id",
        "cell_id",
        "cell name",
        "cellname",
        "sector"
    ],

    "Technology": [
        "technology",
        "tech",
        "rat",
        "network type"
    ],

    "Availability": [
        "availability",
        "availability (%)",
        "network availability",
        "cell availability"
    ],

    "CSSR": [
        "cssr",
        "cssr (%)",
        "call setup success rate",
        "call setup success"
    ],

    "DCR": [
        "dcr",
        "dcr (%)",
        "dropped call rate",
        "drop call rate",
        "call drop rate"
    ],

    "HOSR": [
        "hosr",
        "hosr (%)",
        "handover success rate",
        "ho success rate"
    ],

    "Traffic": [
        "traffic",
        "traffic (gb)",
        "data traffic",
        "total traffic"
    ],

    "Latency": [
        "latency",
        "latency (ms)",
        "average latency"
    ],

    "Active Users": [
        "active users",
        "active_users",
        "users",
        "subscribers"
    ],


    # --------------------------------------------------------
    # 2G
    # --------------------------------------------------------

    "TCH Traffic": [
        "tch traffic",
        "tch traffic erlang",
        "tch traffic (erl)",
        "voice traffic erlang"
    ],

    "TCH Congestion": [
        "tch congestion",
        "tch congestion (%)",
        "tch congestion rate"
    ],

    "SDCCH Congestion": [
        "sdcch congestion",
        "sdcch congestion (%)",
        "sdcch congestion rate"
    ],

    "SDCCH Success": [
        "sdcch success",
        "sdcch success rate",
        "sdcch success (%)"
    ],


    # --------------------------------------------------------
    # 3G / 4G / 5G
    # --------------------------------------------------------

    "RRC Success": [
        "rrc success",
        "rrc success rate",
        "rrc success (%)",
        "rrc setup success",
        "rrc setup success rate"
    ],

    "RTWP": [
        "rtwp",
        "rtwp dbm",
        "rtwp (dbm)"
    ],

    "ERAB Success": [
        "erab success",
        "e-rab success",
        "erab success rate",
        "e-rab success rate",
        "erab setup success"
    ],

    "Session Success": [
        "session success",
        "session establishment success",
        "pdu session success",
        "pdu session establishment success"
    ],

    "PRB Utilization": [
        "prb utilization",
        "prb utilization (%)",
        "dl prb utilization",
        "resource block utilization"
    ],

    "DL Throughput": [
        "dl throughput",
        "downlink throughput",
        "average dl throughput",
        "dl throughput mbps",
        "dl throughput (mbps)"
    ],


    # --------------------------------------------------------
    # VoLTE
    # --------------------------------------------------------

    "VoLTE CSSR": [
        "volte cssr",
        "volte call setup success",
        "volte call setup success rate",
        "ims cssr"
    ],

    "VoLTE DCR": [
        "volte dcr",
        "volte drop rate",
        "volte call drop rate"
    ],

    "SRVCC Success": [
        "srvcc success",
        "srvcc success rate",
        "srvcc success (%)"
    ],

    "Packet Loss": [
        "packet loss",
        "packet loss (%)",
        "volte packet loss",
        "rtp packet loss"
    ],

    "Voice Traffic": [
        "voice traffic",
        "voice traffic erlang",
        "voice traffic (erl)",
        "volte traffic"
    ]
}


def detect_columns(
    df
):

    detected = {}

    for logical_name, aliases in COLUMN_ALIASES.items():

        detected[
            logical_name
        ] = find_column(
            df,
            aliases
        )

    return detected


# ============================================================
# EXCEL EXPORT
# ============================================================

def dataframe_to_excel_bytes(
    dataframe
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Report"
        )

    output.seek(
        0
    )

    return output.getvalue()


# ============================================================
# DEMO REPORT DATA
# ============================================================

@st.cache_data(ttl=300)
def generate_demo_report_data():

    rng = np.random.default_rng(
        2026
    )

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

    for date in dates:

        for site in sites:

            for technology in technologies:

                base = {

                    "Date":
                        date,

                    "Site":
                        site,

                    "Cell":
                        (
                            f"{site}_"
                            f"{technology}_"
                            f"CELL_{rng.integers(1,4)}"
                        ),

                    "Technology":
                        technology,

                    "Availability":
                        round(
                            float(
                                rng.uniform(
                                    96.5,
                                    99.9
                                )
                            ),
                            2
                        ),

                    "CSSR":
                        round(
                            float(
                                rng.uniform(
                                    96.0,
                                    99.8
                                )
                            ),
                            2
                        ),

                    "DCR":
                        round(
                            float(
                                rng.uniform(
                                    0.3,
                                    2.8
                                )
                            ),
                            2
                        ),

                    "HOSR":
                        round(
                            float(
                                rng.uniform(
                                    94.0,
                                    99.5
                                )
                            ),
                            2
                        ),

                    "Traffic":
                        round(
                            float(
                                rng.uniform(
                                    200,
                                    1400
                                )
                            ),
                            1
                        ),

                    "Latency":
                        round(
                            float(
                                rng.uniform(
                                    20,
                                    55
                                )
                            ),
                            1
                        ),

                    "Active Users":
                        int(
                            rng.integers(
                                500,
                                10000
                            )
                        ),

                    "TCH Traffic":
                        np.nan,

                    "TCH Congestion":
                        np.nan,

                    "SDCCH Congestion":
                        np.nan,

                    "SDCCH Success":
                        np.nan,

                    "RRC Success":
                        np.nan,

                    "RTWP":
                        np.nan,

                    "ERAB Success":
                        np.nan,

                    "Session Success":
                        np.nan,

                    "PRB Utilization":
                        np.nan,

                    "DL Throughput":
                        np.nan,

                    "VoLTE CSSR":
                        np.nan,

                    "VoLTE DCR":
                        np.nan,

                    "SRVCC Success":
                        np.nan,

                    "Packet Loss":
                        np.nan,

                    "Voice Traffic":
                        np.nan
                }


                # =================================================
                # 2G
                # =================================================

                if technology == "2G":

                    base[
                        "TCH Traffic"
                    ] = round(
                        float(
                            rng.uniform(
                                5000,
                                11000
                            )
                        ),
                        0
                    )

                    base[
                        "TCH Congestion"
                    ] = round(
                        float(
                            rng.uniform(
                                0.2,
                                4.0
                            )
                        ),
                        2
                    )

                    base[
                        "SDCCH Congestion"
                    ] = round(
                        float(
                            rng.uniform(
                                0.1,
                                2.5
                            )
                        ),
                        2
                    )

                    base[
                        "SDCCH Success"
                    ] = round(
                        float(
                            rng.uniform(
                                96.0,
                                99.7
                            )
                        ),
                        2
                    )


                # =================================================
                # 3G
                # =================================================

                elif technology == "3G":

                    base[
                        "RRC Success"
                    ] = round(
                        float(
                            rng.uniform(
                                96.5,
                                99.8
                            )
                        ),
                        2
                    )

                    base[
                        "RTWP"
                    ] = round(
                        float(
                            rng.uniform(
                                -108,
                                -85
                            )
                        ),
                        1
                    )


                # =================================================
                # 4G
                # =================================================

                elif technology == "4G":

                    base[
                        "RRC Success"
                    ] = round(
                        float(
                            rng.uniform(
                                97.0,
                                99.9
                            )
                        ),
                        2
                    )

                    base[
                        "ERAB Success"
                    ] = round(
                        float(
                            rng.uniform(
                                96.5,
                                99.8
                            )
                        ),
                        2
                    )

                    base[
                        "PRB Utilization"
                    ] = round(
                        float(
                            rng.uniform(
                                25,
                                82
                            )
                        ),
                        1
                    )

                    base[
                        "DL Throughput"
                    ] = round(
                        float(
                            rng.uniform(
                                20,
                                110
                            )
                        ),
                        1
                    )


                # =================================================
                # 5G
                # =================================================

                elif technology == "5G":

                    base[
                        "RRC Success"
                    ] = round(
                        float(
                            rng.uniform(
                                97.5,
                                99.95
                            )
                        ),
                        2
                    )

                    base[
                        "Session Success"
                    ] = round(
                        float(
                            rng.uniform(
                                97.0,
                                99.9
                            )
                        ),
                        2
                    )

                    base[
                        "PRB Utilization"
                    ] = round(
                        float(
                            rng.uniform(
                                15,
                                75
                            )
                        ),
                        1
                    )

                    base[
                        "DL Throughput"
                    ] = round(
                        float(
                            rng.uniform(
                                80,
                                350
                            )
                        ),
                        1
                    )


                # =================================================
                # VoLTE
                # =================================================

                elif technology == "VoLTE":

                    base[
                        "VoLTE CSSR"
                    ] = round(
                        float(
                            rng.uniform(
                                97.5,
                                99.9
                            )
                        ),
                        2
                    )

                    base[
                        "VoLTE DCR"
                    ] = round(
                        float(
                            rng.uniform(
                                0.1,
                                1.5
                            )
                        ),
                        2
                    )

                    base[
                        "SRVCC Success"
                    ] = round(
                        float(
                            rng.uniform(
                                95.5,
                                99.6
                            )
                        ),
                        2
                    )

                    base[
                        "Packet Loss"
                    ] = round(
                        float(
                            rng.uniform(
                                0.05,
                                1.5
                            )
                        ),
                        2
                    )

                    base[
                        "Voice Traffic"
                    ] = round(
                        float(
                            rng.uniform(
                                1800,
                                6500
                            )
                        ),
                        0
                    )


                rows.append(
                    base
                )

    return pd.DataFrame(
        rows
    )


# ============================================================
# DATA SOURCE
# ============================================================

if "kpi_data" in st.session_state:

    source_df = (
        st.session_state[
            "kpi_data"
        ]
        .copy()
    )

    source_name = (
        st.session_state
        .get(
            "kpi_filename",
            "Uploaded KPI Dataset"
        )
    )

    using_uploaded_data = True

else:

    source_df = (
        generate_demo_report_data()
    )

    source_name = (
        "Demo KPI Dataset"
    )

    using_uploaded_data = False


# ============================================================
# DETECT COLUMNS
# ============================================================

detected_columns = (
    detect_columns(
        source_df
    )
)


date_col = (
    detected_columns[
        "Date"
    ]
)


site_col = (
    detected_columns[
        "Site"
    ]
)


cell_col = (
    detected_columns[
        "Cell"
    ]
)


technology_col = (
    detected_columns[
        "Technology"
    ]
)


availability_col = (
    detected_columns[
        "Availability"
    ]
)


cssr_col = (
    detected_columns[
        "CSSR"
    ]
)


dcr_col = (
    detected_columns[
        "DCR"
    ]
)


hosr_col = (
    detected_columns[
        "HOSR"
    ]
)


traffic_col = (
    detected_columns[
        "Traffic"
    ]
)


latency_col = (
    detected_columns[
        "Latency"
    ]
)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    (
        '<div class="report-wrapper">'
        '<div class="report-title">'
        'Network Report'
        '</div>'
        '<div class="report-subtitle">'
        'Generate, review and export network performance reports'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True
)


# ============================================================
# DATA SOURCE MESSAGE
# ============================================================

if using_uploaded_data:

    st.success(
        f"Using uploaded KPI dataset: {source_name}"
    )

else:

    st.info(
        (
            "No uploaded KPI dataset is currently loaded. "
            "Technology-aware demo data is being used."
        )
    )


# ============================================================
# REPORT FILTERS
# ============================================================

with st.container(
    border=True,
    key="report_panel_filters"
):

    panel_title(
        "Report Filters",
        "Choose the scope of the report"
    )


    filter1, filter2, filter3, filter4 = (
        st.columns(
            4
        )
    )


    # ========================================================
    # REPORT TYPE
    # ========================================================

    with filter1:

        report_type = st.selectbox(
            "Report Type",

            [
                "Network Performance",
                "Technology Performance",
                "Site Performance",
                "KPI Summary"
            ],

            key="report_type"
        )


    # ========================================================
    # SITE
    # ========================================================

    if site_col is not None:

        site_values = sorted(
            source_df[
                site_col
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    else:

        site_values = []


    with filter2:

        selected_site = st.selectbox(
            "Site",

            [
                "All"
            ]
            +
            site_values,

            key="report_site"
        )


    # ========================================================
    # TECHNOLOGY
    # ========================================================

    if technology_col is not None:

        technology_values = sorted(
            source_df[
                technology_col
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    else:

        technology_values = []


    # Ensure telecom order.

    ordered_technologies = [
        technology
        for technology in [
            "2G",
            "3G",
            "4G",
            "5G",
            "VoLTE"
        ]
        if technology
        in technology_values
    ]


    extra_technologies = [
        technology
        for technology
        in technology_values
        if technology
        not in ordered_technologies
    ]


    technology_values = (
        ordered_technologies
        +
        extra_technologies
    )


    with filter3:

        selected_technology = (
            st.selectbox(
                "Technology",

                [
                    "All"
                ]
                +
                technology_values,

                key="report_technology"
            )
        )


    # ========================================================
    # PERIOD
    # ========================================================

    with filter4:

        selected_period = st.selectbox(
            "Period",

            [
                "Last 24 Hours",
                "Last 7 Days",
                "Last 30 Days",
                "All Data"
            ],

            key="report_period"
        )


# ============================================================
# FILTER DATASET
# ============================================================

report_df = (
    source_df.copy()
)


# ============================================================
# SITE FILTER
# ============================================================

if (
    selected_site != "All"
    and
    site_col is not None
):

    report_df = report_df[
        report_df[
            site_col
        ]
        .astype(str)
        ==
        selected_site
    ]


# ============================================================
# TECHNOLOGY FILTER
# ============================================================

if (
    selected_technology != "All"
    and
    technology_col is not None
):

    report_df = report_df[
        report_df[
            technology_col
        ]
        .astype(str)
        ==
        selected_technology
    ]


# ============================================================
# DATE / PERIOD FILTER
# ============================================================

if date_col is not None:

    report_df[
        date_col
    ] = pd.to_datetime(
        report_df[
            date_col
        ],
        errors="coerce"
    )


if (
    selected_period != "All Data"
    and
    date_col is not None
):

    report_df = report_df.dropna(
        subset=[
            date_col
        ]
    )

    if not report_df.empty:

        max_date = report_df[
            date_col
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


        report_df = report_df[
            report_df[
                date_col
            ]
            >=
            start_date
        ]


# ============================================================
# EMPTY RESULT
# ============================================================

if report_df.empty:

    st.warning(
        "No records match the selected report filters."
    )

    st.stop()


# ============================================================
# MAIN KPI VALUES
# ============================================================

availability = safe_numeric_mean(
    report_df,
    availability_col
)


cssr = safe_numeric_mean(
    report_df,
    cssr_col
)


dcr = safe_numeric_mean(
    report_df,
    dcr_col
)


hosr = safe_numeric_mean(
    report_df,
    hosr_col
)


traffic = safe_numeric_mean(
    report_df,
    traffic_col
)


latency = safe_numeric_mean(
    report_df,
    latency_col
)


# ============================================================
# KPI CARDS
# ============================================================

st.write("")


k1, k2, k3, k4, k5, k6 = (
    st.columns(
        6,
        gap="small"
    )
)


with k1:

    report_kpi_card(
        "Availability",

        (
            f"{availability:.2f}%"
            if not pd.isna(
                availability
            )
            else "—"
        ),

        "Average availability",

        "report_kpi_availability"
    )


with k2:

    report_kpi_card(
        "CSSR",

        (
            f"{cssr:.2f}%"
            if not pd.isna(
                cssr
            )
            else "—"
        ),

        "Average CSSR",

        "report_kpi_cssr"
    )


with k3:

    report_kpi_card(
        "DCR",

        (
            f"{dcr:.2f}%"
            if not pd.isna(
                dcr
            )
            else "—"
        ),

        "Average call drop",

        "report_kpi_dcr"
    )


with k4:

    report_kpi_card(
        "HOSR",

        (
            f"{hosr:.2f}%"
            if not pd.isna(
                hosr
            )
            else "—"
        ),

        "Average handover success",

        "report_kpi_hosr"
    )


with k5:

    report_kpi_card(
        "Traffic",

        (
            f"{traffic:,.1f}"
            if not pd.isna(
                traffic
            )
            else "—"
        ),

        "Average traffic",

        "report_kpi_traffic"
    )


with k6:

    report_kpi_card(
        "Latency",

        (
            f"{latency:.1f} ms"
            if not pd.isna(
                latency
            )
            else "—"
        ),

        "Average latency",

        "report_kpi_latency"
    )


# ============================================================
# REPORT SUMMARY
# ============================================================

st.write("")


with st.container(
    border=True,
    key="report_panel_summary"
):

    panel_title(
        "Report Summary",
        "Summary of the currently selected report scope"
    )


    summary1, summary2, summary3, summary4 = (
        st.columns(
            4
        )
    )


    with summary1:

        st.metric(
            "Records",
            f"{len(report_df):,}"
        )


    with summary2:

        if site_col is not None:

            site_count = (
                report_df[
                    site_col
                ]
                .nunique(
                    dropna=True
                )
            )

        else:

            site_count = 0


        st.metric(
            "Sites",
            f"{site_count:,}"
        )


    with summary3:

        if technology_col is not None:

            tech_count = (
                report_df[
                    technology_col
                ]
                .nunique(
                    dropna=True
                )
            )

        else:

            tech_count = 0


        st.metric(
            "Technologies",
            f"{tech_count:,}"
        )


    with summary4:

        st.metric(
            "Report Type",
            report_type
        )


# ============================================================
# REPORT PREVIEW
# ============================================================

st.write("")


with st.container(
    border=True,
    key="report_panel_preview"
):

    panel_title(
        "Report Preview",
        "Filtered network performance dataset"
    )


    preview_rows = st.selectbox(
        "Rows to display",

        [
            25,
            50,
            100,
            250
        ],

        index=1,

        key="report_preview_rows"
    )


    st.dataframe(
        report_df.head(
            preview_rows
        ),

        use_container_width=True,

        hide_index=True,

        height=420
    )


# ============================================================
# GROUPED SUMMARY
# ============================================================

st.write("")


with st.container(
    border=True,
    key="report_panel_grouped_summary"
):

    panel_title(
        "Grouped KPI Summary",
        "Average KPI performance by report dimension"
    )


    group_column = None


    if (
        report_type == "Site Performance"
        and
        site_col is not None
    ):

        group_column = (
            site_col
        )

    elif technology_col is not None:

        group_column = (
            technology_col
        )

    elif site_col is not None:

        group_column = (
            site_col
        )


    numeric_columns = [
        column
        for column in [
            availability_col,
            cssr_col,
            dcr_col,
            hosr_col,
            traffic_col,
            latency_col
        ]
        if column is not None
    ]


    if (
        group_column is not None
        and
        numeric_columns
    ):

        grouped_df = report_df[
            [
                group_column
            ]
            +
            numeric_columns
        ].copy()


        for column in numeric_columns:

            grouped_df[
                column
            ] = pd.to_numeric(
                grouped_df[
                    column
                ],
                errors="coerce"
            )


        grouped_df = (
            grouped_df
            .groupby(
                group_column,
                dropna=False
            )[
                numeric_columns
            ]
            .mean()
            .round(
                2
            )
            .reset_index()
        )


        st.dataframe(
            grouped_df,

            use_container_width=True,

            hide_index=True,

            height=320
        )

    else:

        st.info(
            (
                "The current dataset does not contain enough "
                "recognizable columns to generate a grouped summary."
            )
        )


# ============================================================
# PROFESSIONAL TECHNOLOGY-AWARE PDF
# ============================================================

def dataframe_to_pdf_bytes(
    dataframe,
    report_type,
    selected_site,
    selected_technology,
    selected_period
):

    # ========================================================
    # BRAND COLORS
    # ========================================================

    BLACK = colors.HexColor(
        "#0B0D10"
    )

    DARK = colors.HexColor(
        "#1F2937"
    )

    CORAL = colors.HexColor(
        "#FF6258"
    )

    GREY = colors.HexColor(
        "#667085"
    )

    MUTED = colors.HexColor(
        "#98A2B3"
    )

    LIGHT_GREY = colors.HexColor(
        "#D0D5DD"
    )

    VERY_LIGHT = colors.HexColor(
        "#F8FAFC"
    )

    GREEN = colors.HexColor(
        "#16A34A"
    )

    AMBER = colors.HexColor(
        "#D97706"
    )

    RED = colors.HexColor(
        "#DC2626"
    )

    WHITE = colors.white


    # ========================================================
    # OUTPUT / DOCUMENT
    # ========================================================

    output = BytesIO()

    page_size = landscape(
        A4
    )


    document = SimpleDocTemplate(
        output,

        pagesize=page_size,

        rightMargin=12 * mm,
        leftMargin=12 * mm,

        topMargin=22 * mm,
        bottomMargin=17 * mm,

        title=(
            "Network Operations "
            "Performance Report"
        ),

        author=(
            "Network Operations"
        )
    )


    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "ExecutiveTitle",

        parent=styles[
            "Title"
        ],

        fontName="Helvetica-Bold",

        fontSize=24,

        leading=29,

        textColor=BLACK,

        alignment=TA_LEFT,

        spaceAfter=2 * mm
    )


    subtitle_style = ParagraphStyle(
        "ExecutiveSubtitle",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica",

        fontSize=9.5,

        leading=13,

        textColor=GREY,

        spaceAfter=3 * mm
    )


    section_title_style = ParagraphStyle(
        "SectionTitle",

        parent=styles[
            "Heading2"
        ],

        fontName="Helvetica-Bold",

        fontSize=14,

        leading=17,

        textColor=BLACK,

        spaceAfter=2.5 * mm
    )


    section_subtitle_style = ParagraphStyle(
        "SectionSubtitle",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica",

        fontSize=8.5,

        leading=12,

        textColor=GREY,

        spaceAfter=3 * mm
    )


    body_style = ParagraphStyle(
        "ProfessionalBody",

        parent=styles[
            "BodyText"
        ],

        fontName="Helvetica",

        fontSize=9,

        leading=13,

        textColor=DARK
    )


    small_style = ParagraphStyle(
        "SmallText",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica",

        fontSize=7,

        leading=9,

        textColor=GREY
    )


    table_header_style = ParagraphStyle(
        "TableHeader",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica-Bold",

        fontSize=6.8,

        leading=8,

        textColor=WHITE,

        alignment=TA_CENTER
    )


    table_cell_style = ParagraphStyle(
        "TableCell",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica",

        fontSize=6.6,

        leading=8,

        textColor=DARK,

        alignment=TA_CENTER
    )


    kpi_label_style = ParagraphStyle(
        "KpiLabel",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica-Bold",

        fontSize=6.8,

        leading=8,

        textColor=GREY
    )


    kpi_value_style = ParagraphStyle(
        "KpiValue",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica-Bold",

        fontSize=15,

        leading=17,

        textColor=BLACK
    )


    kpi_note_style = ParagraphStyle(
        "KpiNote",

        parent=styles[
            "Normal"
        ],

        fontName="Helvetica-Bold",

        fontSize=6.5,

        leading=8,

        textColor=GREY
    )


    # ========================================================
    # LOCAL COLUMN DETECTION
    # ========================================================

    columns = detect_columns(
        dataframe
    )


    date_pdf_col = (
        columns[
            "Date"
        ]
    )


    site_pdf_col = (
        columns[
            "Site"
        ]
    )


    cell_pdf_col = (
        columns[
            "Cell"
        ]
    )


    technology_pdf_col = (
        columns[
            "Technology"
        ]
    )


    # ========================================================
    # HEADER / FOOTER
    # ========================================================

    def draw_header_footer(
        canvas,
        doc
    ):

        canvas.saveState()

        page_width, page_height = (
            page_size
        )


        # ----------------------------------------------------
        # BLACK HEADER
        # ----------------------------------------------------

        canvas.setFillColor(
            BLACK
        )

        canvas.rect(
            0,
            page_height - 14 * mm,
            page_width,
            14 * mm,
            fill=1,
            stroke=0
        )


        canvas.setFillColor(
            WHITE
        )

        canvas.setFont(
            "Helvetica-Bold",
            11
        )

        canvas.drawString(
            12 * mm,
            page_height - 9 * mm,
            "NETWORK OPS"
        )


        canvas.setFont(
            "Helvetica",
            7
        )

        canvas.drawRightString(
            page_width - 12 * mm,
            page_height - 9 * mm,
            (
                "NETWORK OPERATIONS "
                "PERFORMANCE REPORT"
            )
        )


        # ----------------------------------------------------
        # CORAL ACCENT
        # ----------------------------------------------------

        canvas.setFillColor(
            CORAL
        )

        canvas.rect(
            0,
            page_height - 15.5 * mm,
            page_width,
            1.5 * mm,
            fill=1,
            stroke=0
        )


        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        canvas.setStrokeColor(
            LIGHT_GREY
        )

        canvas.line(
            12 * mm,
            12 * mm,
            page_width - 12 * mm,
            12 * mm
        )


        canvas.setFillColor(
            GREY
        )

        canvas.setFont(
            "Helvetica",
            7
        )


        canvas.drawString(
            12 * mm,
            7 * mm,
            (
                "CONFIDENTIAL - "
                "Network Operations"
            )
        )


        canvas.drawRightString(
            page_width - 12 * mm,
            7 * mm,
            f"Page {doc.page}"
        )


        canvas.restoreState()


    # ========================================================
    # FORMATTER
    # ========================================================

    def format_number(
        value,
        unit="",
        decimals=2
    ):

        if (
            value is None
            or
            pd.isna(
                value
            )
        ):

            return "N/A"

        return (
            f"{value:,.{decimals}f}"
            f"{unit}"
        )


    # ========================================================
    # STATUS
    # ========================================================

    def success_status(
        metric,
        value
    ):

        if pd.isna(
            value
        ):

            return (
                "N/A",
                GREY
            )


        lower_metric = (
            metric.lower()
        )


        if (
            "dcr"
            in lower_metric
            or
            "drop"
            in lower_metric
        ):

            if value <= 2:

                return (
                    "GOOD",
                    GREEN
                )

            elif value <= 3:

                return (
                    "WATCH",
                    AMBER
                )

            return (
                "CRITICAL",
                RED
            )


        if (
            "congestion"
            in lower_metric
            or
            "packet loss"
            in lower_metric
        ):

            if value <= 2:

                return (
                    "GOOD",
                    GREEN
                )

            elif value <= 5:

                return (
                    "WATCH",
                    AMBER
                )

            return (
                "CRITICAL",
                RED
            )


        if (
            "latency"
            in lower_metric
        ):

            if value <= 40:

                return (
                    "GOOD",
                    GREEN
                )

            elif value <= 60:

                return (
                    "WATCH",
                    AMBER
                )

            return (
                "CRITICAL",
                RED
            )


        if (
            "availability"
            in lower_metric
        ):

            if value >= 98:

                return (
                    "GOOD",
                    GREEN
                )

            elif value >= 95:

                return (
                    "WATCH",
                    AMBER
                )

            return (
                "CRITICAL",
                RED
            )


        if (
            "success"
            in lower_metric
            or
            "cssr"
            in lower_metric
            or
            "hosr"
            in lower_metric
        ):

            if value >= 97:

                return (
                    "GOOD",
                    GREEN
                )

            elif value >= 94:

                return (
                    "WATCH",
                    AMBER
                )

            return (
                "CRITICAL",
                RED
            )


        return (
            "INFO",
            GREY
        )


    # ========================================================
    # KPI CARD TABLE
    # ========================================================

    def build_kpi_cards(
        kpis
    ):

        cells = []

        for (
            label,
            value,
            unit,
            decimals
        ) in kpis:

            status_text, status_color = (
                success_status(
                    label,
                    value
                )
            )


            cells.append(
                [
                    Paragraph(
                        label.upper(),
                        kpi_label_style
                    ),

                    Spacer(
                        1,
                        1 * mm
                    ),

                    Paragraph(
                        format_number(
                            value,
                            unit,
                            decimals
                        ),
                        kpi_value_style
                    ),

                    Spacer(
                        1,
                        0.5 * mm
                    ),

                    Paragraph(
                        (
                            f'<font color="'
                            f'{status_color.hexval()}">'
                            f'{status_text}'
                            f'</font>'
                        ),
                        kpi_note_style
                    )
                ]
            )


        available_width = (
            page_size[
                0
            ]
            -
            24 * mm
        )


        width = (
            available_width
            /
            len(
                cells
            )
        )


        table = Table(
            [
                cells
            ],
            colWidths=[
                width
            ]
            *
            len(
                cells
            )
        )


        table.setStyle(
            TableStyle(
                [
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        WHITE
                    ),

                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.8,
                        LIGHT_GREY
                    ),

                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.8,
                        LIGHT_GREY
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    )
                ]
            )
        )


        return table


    # ========================================================
    # PROFESSIONAL TABLE
    # ========================================================

    def professional_table(
        source_df,
        max_rows=20
    ):

        table_df = (
            source_df
            .head(
                max_rows
            )
            .copy()
        )


        for column in table_df.columns:

            if pd.api.types.is_datetime64_any_dtype(
                table_df[
                    column
                ]
            ):

                table_df[
                    column
                ] = (
                    table_df[
                        column
                    ]
                    .dt
                    .strftime(
                        "%d %b %Y"
                    )
                )


            elif pd.api.types.is_float_dtype(
                table_df[
                    column
                ]
            ):

                table_df[
                    column
                ] = (
                    table_df[
                        column
                    ]
                    .round(
                        2
                    )
                )


        header = [
            Paragraph(
                str(column),
                table_header_style
            )
            for column
            in table_df.columns
        ]


        rows = [
            header
        ]


        for row in (
            table_df
            .astype(str)
            .values
            .tolist()
        ):

            rows.append(
                [
                    Paragraph(
                        str(value),
                        table_cell_style
                    )
                    for value
                    in row
                ]
            )


        available_width = (
            page_size[
                0
            ]
            -
            24 * mm
        )


        column_count = max(
            len(
                table_df.columns
            ),
            1
        )


        table = Table(
            rows,

            repeatRows=1,

            colWidths=[
                (
                    available_width
                    /
                    column_count
                )
            ]
            *
            column_count
        )


        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        BLACK
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        WHITE
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.45,
                        LIGHT_GREY
                    ),

                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            WHITE,
                            VERY_LIGHT
                        ]
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    )
                ]
            )
        )


        return table


    # ========================================================
    # SIMPLE KPI TREND
    # ========================================================

    def trend_chart(
        tech_df,
        metrics
    ):

        if date_pdf_col is None:

            return None


        temp = (
            tech_df
            .copy()
        )


        temp[
            date_pdf_col
        ] = pd.to_datetime(
            temp[
                date_pdf_col
            ],
            errors="coerce"
        )


        temp = temp.dropna(
            subset=[
                date_pdf_col
            ]
        )


        usable = []


        for (
            metric_name,
            logical_name
        ) in metrics:

            column = columns.get(
                logical_name
            )


            if column is not None:

                temp[
                    column
                ] = pd.to_numeric(
                    temp[
                        column
                    ],
                    errors="coerce"
                )


                if temp[
                    column
                ].notna().any():

                    usable.append(
                        (
                            metric_name,
                            column
                        )
                    )


        if (
            not usable
            or
            temp.empty
        ):

            return None


        selected_columns = [
            column
            for _, column
            in usable
        ]


        daily = (
            temp
            .groupby(
                temp[
                    date_pdf_col
                ]
                .dt
                .floor("D")
            )[
                selected_columns
            ]
            .mean()
            .reset_index()
            .tail(
                20
            )
        )


        drawing = Drawing(
            690,
            170
        )


        chart = HorizontalLineChart()


        chart.x = 48
        chart.y = 32

        chart.width = 610
        chart.height = 100


        chart.data = [

            daily[
                column
            ]
            .fillna(
                0
            )
            .tolist()

            for _, column
            in usable
        ]


        chart.categoryAxis.categoryNames = [

            value.strftime(
                "%d %b"
            )

            for value
            in daily[
                date_pdf_col
            ]
        ]


        chart.categoryAxis.labels.fontSize = 5.5

        chart.categoryAxis.labels.angle = 35


        chart.valueAxis.labels.fontSize = 6


        line_colors = [
            CORAL,
            BLACK,
            colors.HexColor(
                "#475467"
            ),
            colors.HexColor(
                "#1570EF"
            )
        ]


        for index in range(
            len(
                usable
            )
        ):

            chart.lines[
                index
            ].strokeColor = (
                line_colors[
                    index
                    %
                    len(
                        line_colors
                    )
                ]
            )


            chart.lines[
                index
            ].strokeWidth = 1.7


            chart.lines[
                index
            ].symbol = makeMarker(
                "FilledCircle"
            )


            chart.lines[
                index
            ].symbol.size = 3


        drawing.add(
            chart
        )


        legend_x = 50


        for index, (
            metric_name,
            _
        ) in enumerate(
            usable
        ):

            drawing.add(
                String(
                    legend_x,
                    152,

                    metric_name,

                    fontSize=7,

                    fillColor=(
                        line_colors[
                            index
                            %
                            len(
                                line_colors
                            )
                        ]
                    )
                )
            )

            legend_x += 120


        return drawing


    # ========================================================
    # TECHNOLOGY CONFIG
    # ========================================================

    technology_profiles = {

        "2G": {

            "title":
                "2G / GSM Performance",

            "subtitle":
                (
                    "Voice accessibility, retainability, "
                    "mobility and GSM capacity performance."
                ),

            "kpis": [

                (
                    "Availability",
                    "Availability",
                    "%",
                    2
                ),

                (
                    "CSSR",
                    "CSSR",
                    "%",
                    2
                ),

                (
                    "DCR",
                    "DCR",
                    "%",
                    2
                ),

                (
                    "HOSR",
                    "HOSR",
                    "%",
                    2
                ),

                (
                    "TCH Traffic",
                    "TCH Traffic",
                    " Erl",
                    0
                ),

                (
                    "TCH Congestion",
                    "TCH Congestion",
                    "%",
                    2
                ),

                (
                    "SDCCH Congestion",
                    "SDCCH Congestion",
                    "%",
                    2
                )
            ],

            "trend": [

                (
                    "Availability",
                    "Availability"
                ),

                (
                    "CSSR",
                    "CSSR"
                ),

                (
                    "HOSR",
                    "HOSR"
                )
            ]
        },


        "3G": {

            "title":
                "3G / UMTS Performance",

            "subtitle":
                (
                    "UMTS accessibility, retainability, "
                    "mobility, interference and traffic."
                ),

            "kpis": [

                (
                    "Availability",
                    "Availability",
                    "%",
                    2
                ),

                (
                    "CSSR",
                    "CSSR",
                    "%",
                    2
                ),

                (
                    "DCR",
                    "DCR",
                    "%",
                    2
                ),

                (
                    "HOSR",
                    "HOSR",
                    "%",
                    2
                ),

                (
                    "RRC Success",
                    "RRC Success",
                    "%",
                    2
                ),

                (
                    "Traffic",
                    "Traffic",
                    "",
                    1
                ),

                (
                    "RTWP",
                    "RTWP",
                    " dBm",
                    1
                )
            ],

            "trend": [

                (
                    "Availability",
                    "Availability"
                ),

                (
                    "CSSR",
                    "CSSR"
                ),

                (
                    "RRC Success",
                    "RRC Success"
                )
            ]
        },


        "4G": {

            "title":
                "4G / LTE Performance",

            "subtitle":
                (
                    "LTE accessibility, bearer setup, "
                    "mobility, throughput and capacity."
                ),

            "kpis": [

                (
                    "Availability",
                    "Availability",
                    "%",
                    2
                ),

                (
                    "RRC Success",
                    "RRC Success",
                    "%",
                    2
                ),

                (
                    "ERAB Success",
                    "ERAB Success",
                    "%",
                    2
                ),

                (
                    "HOSR",
                    "HOSR",
                    "%",
                    2
                ),

                (
                    "Traffic",
                    "Traffic",
                    "",
                    1
                ),

                (
                    "DL Throughput",
                    "DL Throughput",
                    " Mbps",
                    1
                ),

                (
                    "PRB Utilization",
                    "PRB Utilization",
                    "%",
                    1
                ),

                (
                    "Latency",
                    "Latency",
                    " ms",
                    1
                )
            ],

            "trend": [

                (
                    "Availability",
                    "Availability"
                ),

                (
                    "RRC Success",
                    "RRC Success"
                ),

                (
                    "ERAB Success",
                    "ERAB Success"
                ),

                (
                    "HOSR",
                    "HOSR"
                )
            ]
        },


        "5G": {

            "title":
                "5G / NR Performance",

            "subtitle":
                (
                    "5G NR accessibility, session setup, "
                    "mobility, capacity and user throughput."
                ),

            "kpis": [

                (
                    "Availability",
                    "Availability",
                    "%",
                    2
                ),

                (
                    "RRC Success",
                    "RRC Success",
                    "%",
                    2
                ),

                (
                    "Session Success",
                    "Session Success",
                    "%",
                    2
                ),

                (
                    "HOSR",
                    "HOSR",
                    "%",
                    2
                ),

                (
                    "Traffic",
                    "Traffic",
                    "",
                    1
                ),

                (
                    "DL Throughput",
                    "DL Throughput",
                    " Mbps",
                    1
                ),

                (
                    "PRB Utilization",
                    "PRB Utilization",
                    "%",
                    1
                ),

                (
                    "Active Users",
                    "Active Users",
                    "",
                    0
                )
            ],

            "trend": [

                (
                    "Availability",
                    "Availability"
                ),

                (
                    "RRC Success",
                    "RRC Success"
                ),

                (
                    "Session Success",
                    "Session Success"
                ),

                (
                    "HOSR",
                    "HOSR"
                )
            ]
        },


        "VoLTE": {

            "title":
                "VoLTE Service Performance",

            "subtitle":
                (
                    "VoLTE call accessibility, retainability, "
                    "mobility, packet quality and voice traffic."
                ),

            "kpis": [

                (
                    "Availability",
                    "Availability",
                    "%",
                    2
                ),

                (
                    "Call Setup Success",
                    "VoLTE CSSR",
                    "%",
                    2
                ),

                (
                    "Call Drop Rate",
                    "VoLTE DCR",
                    "%",
                    2
                ),

                (
                    "HOSR",
                    "HOSR",
                    "%",
                    2
                ),

                (
                    "SRVCC Success",
                    "SRVCC Success",
                    "%",
                    2
                ),

                (
                    "Packet Loss",
                    "Packet Loss",
                    "%",
                    2
                ),

                (
                    "Voice Traffic",
                    "Voice Traffic",
                    " Erl",
                    0
                )
            ],

            "trend": [

                (
                    "Call Setup Success",
                    "VoLTE CSSR"
                ),

                (
                    "SRVCC Success",
                    "SRVCC Success"
                ),

                (
                    "HOSR",
                    "HOSR"
                )
            ]
        }
    }


    # ========================================================
    # BUILD TECHNOLOGY DATA
    # ========================================================

    def technology_dataframe(
        technology
    ):

        if technology_pdf_col is None:

            return dataframe.copy()


        normalized_series = (

            dataframe[
                technology_pdf_col
            ]
            .astype(str)
            .str.strip()
            .str.lower()
        )


        technology_aliases = {

            "2G": [
                "2g",
                "gsm"
            ],

            "3G": [
                "3g",
                "umts",
                "wcdma"
            ],

            "4G": [
                "4g",
                "lte"
            ],

            "5G": [
                "5g",
                "nr",
                "5g nr"
            ],

            "VoLTE": [
                "volte",
                "voice over lte",
                "ims"
            ]
        }


        accepted = [

            value.lower()

            for value
            in technology_aliases[
                technology
            ]
        ]


        return dataframe[
            normalized_series.isin(
                accepted
            )
        ].copy()


    # ========================================================
    # EXECUTIVE SUMMARY KPIS
    # ========================================================

    overall_availability = (
        safe_numeric_mean(
            dataframe,
            columns[
                "Availability"
            ]
        )
    )


    overall_cssr = (
        safe_numeric_mean(
            dataframe,
            columns[
                "CSSR"
            ]
        )
    )


    overall_dcr = (
        safe_numeric_mean(
            dataframe,
            columns[
                "DCR"
            ]
        )
    )


    overall_hosr = (
        safe_numeric_mean(
            dataframe,
            columns[
                "HOSR"
            ]
        )
    )


    overall_traffic = (
        safe_numeric_mean(
            dataframe,
            columns[
                "Traffic"
            ]
        )
    )


    overall_latency = (
        safe_numeric_mean(
            dataframe,
            columns[
                "Latency"
            ]
        )
    )


    # ========================================================
    # EXECUTIVE HEALTH
    # ========================================================

    health_flags = []


    if not pd.isna(
        overall_availability
    ):

        health_flags.append(
            overall_availability
            >=
            98
        )


    if not pd.isna(
        overall_dcr
    ):

        health_flags.append(
            overall_dcr
            <=
            2
        )


    if not pd.isna(
        overall_latency
    ):

        health_flags.append(
            overall_latency
            <=
            40
        )


    if (
        health_flags
        and
        all(
            health_flags
        )
    ):

        network_health = (
            "HEALTHY"
        )

        network_health_color = (
            GREEN
        )


    elif (
        health_flags
        and
        not any(
            health_flags
        )
    ):

        network_health = (
            "CRITICAL"
        )

        network_health_color = (
            RED
        )


    else:

        network_health = (
            "MONITOR"
        )

        network_health_color = (
            AMBER
        )


    # ========================================================
    # STORY
    # ========================================================

    story = []


    # ========================================================
    # PAGE 1 - EXECUTIVE SUMMARY
    # ========================================================

    story.append(
        Spacer(
            1,
            7 * mm
        )
    )


    story.append(
        Paragraph(
            (
                "Network Operations "
                "Performance Report"
            ),
            title_style
        )
    )


    story.append(
        Paragraph(
            (
                f"{report_type} | "
                f"Site: {selected_site} | "
                f"Technology: {selected_technology} | "
                f"Period: {selected_period}"
            ),
            subtitle_style
        )
    )


    generated_at = (
        pd.Timestamp.now()
        .strftime(
            "%d %b %Y %H:%M"
        )
    )


    status_table = Table(
        [
            [
                Paragraph(
                    "<b>NETWORK HEALTH</b>",
                    small_style
                ),

                Paragraph(
                    (
                        f'<font color="'
                        f'{network_health_color.hexval()}">'
                        f'<b>{network_health}</b>'
                        f'</font>'
                    ),
                    body_style
                ),

                Paragraph(
                    (
                        f"<b>{len(dataframe):,}</b> "
                        f"filtered records"
                    ),
                    body_style
                ),

                Paragraph(
                    (
                        f"Generated "
                        f"{generated_at}"
                    ),
                    small_style
                )
            ]
        ],

        colWidths=[
            35 * mm,
            45 * mm,
            55 * mm,
            95 * mm
        ]
    )


    status_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    VERY_LIGHT
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    LIGHT_GREY
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )


    story.append(
        status_table
    )


    story.append(
        Spacer(
            1,
            4 * mm
        )
    )


    story.append(
        build_kpi_cards(
            [
                (
                    "Availability",
                    overall_availability,
                    "%",
                    2
                ),

                (
                    "CSSR",
                    overall_cssr,
                    "%",
                    2
                ),

                (
                    "DCR",
                    overall_dcr,
                    "%",
                    2
                ),

                (
                    "HOSR",
                    overall_hosr,
                    "%",
                    2
                ),

                (
                    "Traffic",
                    overall_traffic,
                    "",
                    1
                ),

                (
                    "Latency",
                    overall_latency,
                    " ms",
                    1
                )
            ]
        )
    )


    story.append(
        Spacer(
            1,
            5 * mm
        )
    )


    story.append(
        Paragraph(
            "Executive Summary",
            section_title_style
        )
    )


    summary_parts = []


    if not pd.isna(
        overall_availability
    ):

        summary_parts.append(
            (
                f"Network availability averaged "
                f"{overall_availability:.2f}%."
            )
        )


    if not pd.isna(
        overall_cssr
    ):

        summary_parts.append(
            (
                f"Call setup success averaged "
                f"{overall_cssr:.2f}%."
            )
        )


    if not pd.isna(
        overall_dcr
    ):

        summary_parts.append(
            (
                f"Dropped call rate averaged "
                f"{overall_dcr:.2f}%."
            )
        )


    if not pd.isna(
        overall_hosr
    ):

        summary_parts.append(
            (
                f"Handover success averaged "
                f"{overall_hosr:.2f}%."
            )
        )


    if (
        network_health
        ==
        "HEALTHY"
    ):

        summary_parts.append(
            (
                "The recognized network-level indicators "
                "are broadly within the monitoring thresholds "
                "used by this report."
            )
        )


    elif (
        network_health
        ==
        "CRITICAL"
    ):

        summary_parts.append(
            (
                "Multiple recognized network indicators "
                "require engineering investigation."
            )
        )


    else:

        summary_parts.append(
            (
                "Performance remains operational but one or "
                "more indicators should be monitored."
            )
        )


    story.append(
        Paragraph(
            " ".join(
                summary_parts
            ),
            body_style
        )
    )


    # ========================================================
    # PAGE 2 - TECHNOLOGY EXECUTIVE SUMMARY
    # ========================================================

    technology_sections = []


    if (
        selected_technology
        ==
        "All"
    ):

        technology_sections = [
            "2G",
            "3G",
            "4G",
            "5G",
            "VoLTE"
        ]


    elif (
        selected_technology
        in technology_profiles
    ):

        technology_sections = [
            selected_technology
        ]


    # Technology summary when multiple technologies selected.

    if (
        len(
            technology_sections
        )
        >
        1
    ):

        tech_summary_rows = []


        for technology in (
            technology_sections
        ):

            tech_df = (
                technology_dataframe(
                    technology
                )
            )


            if tech_df.empty:

                continue


            tech_availability = (
                safe_numeric_mean(
                    tech_df,
                    columns[
                        "Availability"
                    ]
                )
            )


            if technology == "2G":

                accessibility = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "CSSR"
                        ]
                    )
                )

                retainability = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "DCR"
                        ]
                    )
                )


            elif technology == "VoLTE":

                accessibility = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "VoLTE CSSR"
                        ]
                    )
                )

                retainability = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "VoLTE DCR"
                        ]
                    )
                )


            elif technology in [
                "4G",
                "5G"
            ]:

                accessibility = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "RRC Success"
                        ]
                    )
                )

                retainability = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            (
                                "ERAB Success"
                                if technology
                                ==
                                "4G"
                                else
                                "Session Success"
                            )
                        ]
                    )
                )


            else:

                accessibility = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "CSSR"
                        ]
                    )
                )

                retainability = (
                    safe_numeric_mean(
                        tech_df,
                        columns[
                            "DCR"
                        ]
                    )
                )


            mobility = (
                safe_numeric_mean(
                    tech_df,
                    columns[
                        "HOSR"
                    ]
                )
            )


            technology_status, _ = (
                success_status(
                    "Availability",
                    tech_availability
                )
            )


            tech_summary_rows.append(
                {

                    "Technology":
                        technology,

                    "Availability":
                        format_number(
                            tech_availability,
                            "%",
                            2
                        ),

                    "Accessibility":
                        format_number(
                            accessibility,
                            "%",
                            2
                        ),

                    "Retainability":
                        format_number(
                            retainability,
                            "%",
                            2
                        ),

                    "Mobility":
                        format_number(
                            mobility,
                            "%",
                            2
                        ),

                    "Status":
                        technology_status
                }
            )


        if tech_summary_rows:

            story.append(
                PageBreak()
            )


            story.append(
                Paragraph(
                    "Technology Executive Summary",
                    section_title_style
                )
            )


            story.append(
                Paragraph(
                    (
                        "Consolidated performance comparison "
                        "across 2G, 3G, 4G, 5G and VoLTE."
                    ),
                    section_subtitle_style
                )
            )


            story.append(
                professional_table(
                    pd.DataFrame(
                        tech_summary_rows
                    ),
                    max_rows=10
                )
            )


    # ========================================================
    # TECHNOLOGY-SPECIFIC PAGES
    # ========================================================

    for technology in (
        technology_sections
    ):

        profile = (
            technology_profiles[
                technology
            ]
        )


        tech_df = (
            technology_dataframe(
                technology
            )
        )


        if tech_df.empty:

            continue


        usable_kpis = []


        for (
            display_name,
            logical_name,
            unit,
            decimals
        ) in profile[
            "kpis"
        ]:

            column = (
                columns.get(
                    logical_name
                )
            )


            value = (
                safe_numeric_mean(
                    tech_df,
                    column
                )
            )


            if not pd.isna(
                value
            ):

                usable_kpis.append(
                    (
                        display_name,
                        value,
                        unit,
                        decimals
                    )
                )


        story.append(
            PageBreak()
        )


        story.append(
            Paragraph(
                profile[
                    "title"
                ],
                section_title_style
            )
        )


        story.append(
            Paragraph(
                profile[
                    "subtitle"
                ],
                section_subtitle_style
            )
        )


        if usable_kpis:

            # Maximum seven cards per row.

            first_row = (
                usable_kpis[
                    :7
                ]
            )


            story.append(
                build_kpi_cards(
                    first_row
                )
            )


            if (
                len(
                    usable_kpis
                )
                >
                7
            ):

                story.append(
                    Spacer(
                        1,
                        3 * mm
                    )
                )

                story.append(
                    build_kpi_cards(
                        usable_kpis[
                            7:
                        ]
                    )
                )


        story.append(
            Spacer(
                1,
                4 * mm
            )
        )


        chart = trend_chart(
            tech_df,
            profile[
                "trend"
            ]
        )


        if chart is not None:

            story.append(
                Paragraph(
                    (
                        f"{technology} "
                        f"Performance Trend"
                    ),
                    section_title_style
                )
            )

            story.append(
                chart
            )


        # ====================================================
        # WORST PERFORMERS
        # ====================================================

        exception_columns = []


        for column in [
            site_pdf_col,
            cell_pdf_col,
            columns[
                "Availability"
            ],
            columns[
                "CSSR"
            ],
            columns[
                "DCR"
            ],
            columns[
                "HOSR"
            ]
        ]:

            if (
                column is not None
                and
                column not in exception_columns
            ):

                exception_columns.append(
                    column
                )


        if exception_columns:

            worst_df = (
                tech_df[
                    exception_columns
                ]
                .copy()
            )


            if (
                columns[
                    "Availability"
                ]
                is not None
            ):

                worst_df[
                    columns[
                        "Availability"
                    ]
                ] = pd.to_numeric(
                    worst_df[
                        columns[
                            "Availability"
                        ]
                    ],
                    errors="coerce"
                )


            if (
                columns[
                    "DCR"
                ]
                is not None
            ):

                worst_df[
                    columns[
                        "DCR"
                    ]
                ] = pd.to_numeric(
                    worst_df[
                        columns[
                            "DCR"
                        ]
                    ],
                    errors="coerce"
                )


            sort_columns = []

            sort_direction = []


            if (
                columns[
                    "Availability"
                ]
                is not None
            ):

                sort_columns.append(
                    columns[
                        "Availability"
                    ]
                )

                sort_direction.append(
                    True
                )


            if (
                columns[
                    "DCR"
                ]
                is not None
            ):

                sort_columns.append(
                    columns[
                        "DCR"
                    ]
                )

                sort_direction.append(
                    False
                )


            if sort_columns:

                worst_df = (
                    worst_df
                    .sort_values(
                        sort_columns,
                        ascending=sort_direction,
                        na_position="last"
                    )
                )


            if (
                site_pdf_col
                is not None
            ):

                worst_df = (
                    worst_df
                    .drop_duplicates(
                        subset=[
                            site_pdf_col
                        ]
                    )
                )


            worst_df = (
                worst_df
                .head(
                    10
                )
            )


            if not worst_df.empty:

                story.append(
                    Spacer(
                        1,
                        4 * mm
                    )
                )


                story.append(
                    Paragraph(
                        (
                            f"Top 10 Worst Performing "
                            f"{technology} Sites / Cells"
                        ),
                        section_title_style
                    )
                )


                story.append(
                    professional_table(
                        worst_df,
                        max_rows=10
                    )
                )


    # ========================================================
    # NETWORK EXCEPTIONS
    # ========================================================

    exception_columns = []


    for column in [
        site_pdf_col,
        cell_pdf_col,
        technology_pdf_col,
        columns[
            "Availability"
        ],
        columns[
            "CSSR"
        ],
        columns[
            "DCR"
        ],
        columns[
            "HOSR"
        ],
        columns[
            "Latency"
        ]
    ]:

        if (
            column is not None
            and
            column not in exception_columns
        ):

            exception_columns.append(
                column
            )


    if exception_columns:

        network_exceptions = (
            dataframe[
                exception_columns
            ]
            .copy()
        )


        if (
            columns[
                "Availability"
            ]
            is not None
        ):

            network_exceptions[
                columns[
                    "Availability"
                ]
            ] = pd.to_numeric(
                network_exceptions[
                    columns[
                        "Availability"
                    ]
                ],
                errors="coerce"
            )


        if (
            columns[
                "DCR"
            ]
            is not None
        ):

            network_exceptions[
                columns[
                    "DCR"
                ]
            ] = pd.to_numeric(
                network_exceptions[
                    columns[
                        "DCR"
                    ]
                ],
                errors="coerce"
            )


        sort_columns = []

        sort_direction = []


        if (
            columns[
                "Availability"
            ]
            is not None
        ):

            sort_columns.append(
                columns[
                    "Availability"
                ]
            )

            sort_direction.append(
                True
            )


        if (
            columns[
                "DCR"
            ]
            is not None
        ):

            sort_columns.append(
                columns[
                    "DCR"
                ]
            )

            sort_direction.append(
                False
            )


        if sort_columns:

            network_exceptions = (
                network_exceptions
                .sort_values(
                    sort_columns,
                    ascending=sort_direction,
                    na_position="last"
                )
            )


        if site_pdf_col is not None:

            network_exceptions = (
                network_exceptions
                .drop_duplicates(
                    subset=[
                        site_pdf_col
                    ]
                )
            )


        network_exceptions = (
            network_exceptions
            .head(
                15
            )
        )


        if not network_exceptions.empty:

            story.append(
                PageBreak()
            )


            story.append(
                Paragraph(
                    "Network Performance Exceptions",
                    section_title_style
                )
            )


            story.append(
                Paragraph(
                    (
                        "Cross-technology ranking of the sites "
                        "or cells requiring the highest level "
                        "of engineering attention."
                    ),
                    section_subtitle_style
                )
            )


            story.append(
                professional_table(
                    network_exceptions,
                    max_rows=15
                )
            )


            story.append(
                Spacer(
                    1,
                    5 * mm
                )
            )


            story.append(
                Paragraph(
                    "Recommended Engineering Actions",
                    section_title_style
                )
            )


            action_data = pd.DataFrame(
                [
                    {
                        "Priority":
                            "P1",

                        "Area":
                            "Availability",

                        "Recommended Action":
                            (
                                "Investigate low-availability nodes "
                                "and correlate with transport, power "
                                "and radio alarms."
                            ),

                        "Owner":
                            "RAN / TX"
                    },

                    {
                        "Priority":
                            "P1",

                        "Area":
                            "Retainability",

                        "Recommended Action":
                            (
                                "Review elevated call-drop locations "
                                "for RF, interference, congestion and "
                                "mobility issues."
                            ),

                        "Owner":
                            "RAN Optimization"
                    },

                    {
                        "Priority":
                            "P2",

                        "Area":
                            "Capacity",

                        "Recommended Action":
                            (
                                "Review high PRB, TCH/SDCCH congestion "
                                "or traffic-constrained locations."
                            ),

                        "Owner":
                            "Capacity Planning"
                    },

                    {
                        "Priority":
                            "P2",

                        "Area":
                            "IP Performance",

                        "Recommended Action":
                            (
                                "Investigate high-latency and packet-"
                                "loss nodes against transport KPIs."
                            ),

                        "Owner":
                            "IP / Transmission"
                    }
                ]
            )


            story.append(
                professional_table(
                    action_data,
                    max_rows=10
                )
            )


    # ========================================================
    # DETAILED KPI APPENDIX
    # ========================================================

    story.append(
        PageBreak()
    )


    story.append(
        Paragraph(
            "Detailed KPI Appendix",
            section_title_style
        )
    )


    story.append(
        Paragraph(
            (
                "Filtered source records used to generate "
                "this report. The PDF is capped for "
                "readability; CSV and Excel retain all "
                "filtered records."
            ),
            section_subtitle_style
        )
    )


    appendix_df = (
        dataframe.copy()
    )


    # Preferred columns first.

    preferred_columns = []


    for column in [
        date_pdf_col,
        site_pdf_col,
        cell_pdf_col,
        technology_pdf_col,
        columns[
            "Availability"
        ],
        columns[
            "CSSR"
        ],
        columns[
            "DCR"
        ],
        columns[
            "HOSR"
        ],
        columns[
            "Traffic"
        ],
        columns[
            "Latency"
        ]
    ]:

        if (
            column is not None
            and
            column not in preferred_columns
        ):

            preferred_columns.append(
                column
            )


    for column in appendix_df.columns:

        if (
            column not in preferred_columns
            and
            len(
                preferred_columns
            )
            <
            12
        ):

            preferred_columns.append(
                column
            )


    if preferred_columns:

        appendix_df = appendix_df[
            preferred_columns[
                :12
            ]
        ]


    story.append(
        professional_table(
            appendix_df,
            max_rows=250
        )
    )


    if len(
        dataframe
    ) > 250:

        story.append(
            Spacer(
                1,
                4 * mm
            )
        )


        story.append(
            Paragraph(
                (
                    f"{len(dataframe):,} filtered records "
                    f"were available. The PDF appendix "
                    f"contains the first 250. Download CSV "
                    f"or Excel for the complete dataset."
                ),
                small_style
            )
        )


    story.append(
        Spacer(
            1,
            5 * mm
        )
    )


    story.append(
        Paragraph(
            "Report Methodology",
            section_title_style
        )
    )


    story.append(
        Paragraph(
            (
                "All figures in this report are derived from "
                "the filtered Network Operations dataset. "
                "The PDF automatically detects supported "
                "2G, 3G, 4G, 5G and VoLTE KPI fields. "
                "Sections and KPIs are omitted when the "
                "corresponding data is not present. "
                "Performance thresholds used for the report "
                "status are indicative and should be aligned "
                "with your organization's approved engineering "
                "targets and SLA definitions before production "
                "deployment."
            ),
            body_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story,

        onFirstPage=(
            draw_header_footer
        ),

        onLaterPages=(
            draw_header_footer
        )
    )


    output.seek(
        0
    )


    return output.getvalue()


# ============================================================
# EXPORT SECTION
# ============================================================

st.write("")


with st.container(
    border=True,
    key="report_panel_export"
):

    panel_title(
        "Export Report",
        (
            "Download the currently filtered "
            "network performance report"
        )
    )


    # ========================================================
    # CSV
    # ========================================================

    csv_data = (
        report_df
        .to_csv(
            index=False
        )
        .encode(
            "utf-8"
        )
    )


    # ========================================================
    # EXCEL
    # ========================================================

    excel_data = (
        dataframe_to_excel_bytes(
            report_df
        )
    )


    # ========================================================
    # PROFESSIONAL PDF
    # ========================================================

    pdf_data = (
        dataframe_to_pdf_bytes(
            report_df,
            report_type,
            selected_site,
            selected_technology,
            selected_period
        )
    )


    # ========================================================
    # DOWNLOAD BUTTONS
    # ========================================================

    export1, export2, export3, export4 = (
        st.columns(
            [
                1.0,
                1.0,
                1.0,
                2.0
            ]
        )
    )


    with export1:

        st.download_button(
            "Download CSV",

            data=csv_data,

            file_name=(
                "network_report.csv"
            ),

            mime="text/csv",

            use_container_width=True,

            key="download_report_csv"
        )


    with export2:

        st.download_button(
            "Download Excel",

            data=excel_data,

            file_name=(
                "network_report.xlsx"
            ),

            mime=(
                "application/"
                "vnd.openxmlformats-"
                "officedocument."
                "spreadsheetml.sheet"
            ),

            use_container_width=True,

            key="download_report_excel"
        )


    with export3:

        st.download_button(
            "Download PDF",

            data=pdf_data,

            file_name=(
                "network_operations_"
                "performance_report.pdf"
            ),

            mime="application/pdf",

            use_container_width=True,

            key="download_report_pdf"
        )


    with export4:

        st.caption(
            (
                f"Export contains "
                f"{len(report_df):,} "
                f"filtered record(s)."
            )
        )


# ============================================================
# EXPORT NOTE
# ============================================================

if len(
    report_df
) > 250:

    st.info(
        (
            "The professional PDF appendix contains "
            "the first 250 filtered records for readability. "
            "CSV and Excel contain the complete filtered dataset."
        )
    )