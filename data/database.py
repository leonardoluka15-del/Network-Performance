import sqlite3

from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np


# ============================================================
# DATABASE LOCATION
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATABASE_PATH = (
    PROJECT_ROOT
    /
    "network_kpi.db"
)


# ============================================================
# MASTER TEMPLATE COLUMN MAP
# ============================================================

COLUMN_MAP = {

    # ========================================================
    # IDENTIFIERS
    # ========================================================

    "Time":
        "time",

    "2G BTS":
        "bts_2g",

    "IHS ID":
        "ihs_id",

    "Vendor":
        "vendor",


    # ========================================================
    # 2G
    # ========================================================

    "2G AVAIL(%)":
        "availability_2g",

    "2G Call Setup Success Rate (CS)_MTN(%)":
        "cssr_2g",

    "2G Data Volume (PS UL)(kb)":
        "data_volume_ul_2g_kb",

    "2G DATA (MB)":
        "data_2g_mb",

    "2G Erlang (TCH)_MTN(Erl)":
        "tch_erlang_2g",

    "Congestion Rate (SDCCH)_MTN(%)":
        "sdcch_congestion_2g",

    "Congestion Rate (TCH Sub Perceived)_MTN(%)":
        "tch_congestion_2g",

    "Drop Call Connections (TCH)_MTN(#)":
        "drop_call_connections_2g",

    "Drop Call Rate (SDCCH)_MTN(%)":
        "drop_call_rate_2g",


    # ========================================================
    # 3G
    # ========================================================

    "3G Call Setup Success Rate (CS)_MTN(%)":
        "cssr_3g",

    "3G Data Volume (PS)_MTN(MB)":
        "data_3g_mb",

    "3G Erlang (CS)_MTN(Erl)":
        "erlang_3g",

    "Availability Rate (Cell)_MTN(%)":
        "availability_3g",

    "Handover Success Rate (CS Intra-Freq)_MTN(%)":
        "hosr_3g",

    "Throughput User (PS HSDPA MAC-HS)_MTN(Kbps)":
        "throughput_3g_kbps",


    # ========================================================
    # 4G
    # ========================================================

    "4G AVAIL(%)":
        "availability_4g",

    "4G RRC Setup Success Rate_MTN(%)":
        "rrc_success_4g",

    "4G E-RAB Setup Success Rate_MTN(%)":
        "erab_success_4g",

    "4G Handover Success Rate_MTN(%)":
        "hosr_4g",

    "4G Data Volume_MTN(MB)":
        "data_4g_mb",

    "4G DL Throughput_MTN(Mbps)":
        "dl_throughput_4g_mbps",

    "4G UL Throughput_MTN(Mbps)":
        "ul_throughput_4g_mbps",

    "4G DL PRB Utilization_MTN(%)":
        "dl_prb_utilization_4g",

    "4G UL PRB Utilization_MTN(%)":
        "ul_prb_utilization_4g",

    "4G Active Users_MTN(#)":
        "active_users_4g",

    "4G Latency_MTN(ms)":
        "latency_4g_ms",


    # ========================================================
    # 5G
    # ========================================================

    "5G AVAIL(%)":
        "availability_5g",

    "5G RRC Setup Success Rate_MTN(%)":
        "rrc_success_5g",

    "5G PDU Session Setup Success Rate_MTN(%)":
        "pdu_session_success_5g",

    "5G Handover Success Rate_MTN(%)":
        "hosr_5g",

    "5G Data Volume_MTN(MB)":
        "data_5g_mb",

    "5G DL Throughput_MTN(Mbps)":
        "dl_throughput_5g_mbps",

    "5G UL Throughput_MTN(Mbps)":
        "ul_throughput_5g_mbps",

    "5G DL PRB Utilization_MTN(%)":
        "dl_prb_utilization_5g",

    "5G UL PRB Utilization_MTN(%)":
        "ul_prb_utilization_5g",

    "5G Active Users_MTN(#)":
        "active_users_5g",

    "5G Latency_MTN(ms)":
        "latency_5g_ms",


    # ========================================================
    # VoLTE
    # ========================================================

    "VoLTE AVAIL(%)":
        "availability_volte",

    "VoLTE Call Setup Success Rate_MTN(%)":
        "cssr_volte",

    "VoLTE Call Drop Rate_MTN(%)":
        "dcr_volte",

    "VoLTE Handover Success Rate_MTN(%)":
        "hosr_volte",

    "VoLTE SRVCC Success Rate_MTN(%)":
        "srvcc_success_volte",

    "VoLTE Packet Loss_MTN(%)":
        "packet_loss_volte",

    "VoLTE Voice Traffic_MTN(Erl)":
        "voice_traffic_volte_erlang"
}


# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_IDENTIFIER_COLUMNS = [
    "Time",
    "2G BTS",
    "IHS ID",
    "Vendor"
]


MASTER_TEMPLATE_COLUMNS = list(
    COLUMN_MAP.keys()
)


# ============================================================
# TECHNOLOGY COLUMN GROUPS
# ============================================================

TECHNOLOGY_COLUMNS = {

    "2G": [
        "time",
        "bts_2g",
        "ihs_id",
        "vendor",

        "availability_2g",
        "cssr_2g",
        "data_volume_ul_2g_kb",
        "data_2g_mb",
        "tch_erlang_2g",
        "sdcch_congestion_2g",
        "tch_congestion_2g",
        "drop_call_connections_2g",
        "drop_call_rate_2g"
    ],


    "3G": [
        "time",
        "bts_2g",
        "ihs_id",
        "vendor",

        "cssr_3g",
        "data_3g_mb",
        "erlang_3g",
        "availability_3g",
        "hosr_3g",
        "throughput_3g_kbps"
    ],


    "4G": [
        "time",
        "bts_2g",
        "ihs_id",
        "vendor",

        "availability_4g",
        "rrc_success_4g",
        "erab_success_4g",
        "hosr_4g",
        "data_4g_mb",
        "dl_throughput_4g_mbps",
        "ul_throughput_4g_mbps",
        "dl_prb_utilization_4g",
        "ul_prb_utilization_4g",
        "active_users_4g",
        "latency_4g_ms"
    ],


    "5G": [
        "time",
        "bts_2g",
        "ihs_id",
        "vendor",

        "availability_5g",
        "rrc_success_5g",
        "pdu_session_success_5g",
        "hosr_5g",
        "data_5g_mb",
        "dl_throughput_5g_mbps",
        "ul_throughput_5g_mbps",
        "dl_prb_utilization_5g",
        "ul_prb_utilization_5g",
        "active_users_5g",
        "latency_5g_ms"
    ],


    "VoLTE": [
        "time",
        "bts_2g",
        "ihs_id",
        "vendor",

        "availability_volte",
        "cssr_volte",
        "dcr_volte",
        "hosr_volte",
        "srvcc_success_volte",
        "packet_loss_volte",
        "voice_traffic_volte_erlang"
    ]
}


# ============================================================
# SAFE NUMERIC MEAN
# ============================================================

def safe_numeric_mean(
    dataframe,
    column_name
):

    if (
        dataframe is None
        or dataframe.empty
        or column_name is None
        or column_name not in dataframe.columns
    ):

        return np.nan


    numeric_values = pd.to_numeric(
        dataframe[
            column_name
        ],
        errors="coerce"
    )


    if numeric_values.dropna().empty:

        return np.nan


    return float(
        numeric_values.mean()
    )


# ============================================================
# SAFE NUMERIC SUM
# ============================================================

def safe_numeric_sum(
    dataframe,
    column_name
):

    if (
        dataframe is None
        or dataframe.empty
        or column_name is None
        or column_name not in dataframe.columns
    ):

        return np.nan


    numeric_values = pd.to_numeric(
        dataframe[
            column_name
        ],
        errors="coerce"
    )


    if numeric_values.dropna().empty:

        return np.nan


    return float(
        numeric_values.sum()
    )


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # ========================================================
    # DAILY KPI TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_kpi (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT NOT NULL,

            bts_2g TEXT,

            ihs_id TEXT NOT NULL,

            vendor TEXT,


            /* ================================================
               2G
               ================================================ */

            availability_2g REAL,

            cssr_2g REAL,

            data_volume_ul_2g_kb REAL,

            data_2g_mb REAL,

            tch_erlang_2g REAL,

            sdcch_congestion_2g REAL,

            tch_congestion_2g REAL,

            drop_call_connections_2g REAL,

            drop_call_rate_2g REAL,


            /* ================================================
               3G
               ================================================ */

            cssr_3g REAL,

            data_3g_mb REAL,

            erlang_3g REAL,

            availability_3g REAL,

            hosr_3g REAL,

            throughput_3g_kbps REAL,


            /* ================================================
               4G
               ================================================ */

            availability_4g REAL,

            rrc_success_4g REAL,

            erab_success_4g REAL,

            hosr_4g REAL,

            data_4g_mb REAL,

            dl_throughput_4g_mbps REAL,

            ul_throughput_4g_mbps REAL,

            dl_prb_utilization_4g REAL,

            ul_prb_utilization_4g REAL,

            active_users_4g REAL,

            latency_4g_ms REAL,


            /* ================================================
               5G
               ================================================ */

            availability_5g REAL,

            rrc_success_5g REAL,

            pdu_session_success_5g REAL,

            hosr_5g REAL,

            data_5g_mb REAL,

            dl_throughput_5g_mbps REAL,

            ul_throughput_5g_mbps REAL,

            dl_prb_utilization_5g REAL,

            ul_prb_utilization_5g REAL,

            active_users_5g REAL,

            latency_5g_ms REAL,


            /* ================================================
               VoLTE
               ================================================ */

            availability_volte REAL,

            cssr_volte REAL,

            dcr_volte REAL,

            hosr_volte REAL,

            srvcc_success_volte REAL,

            packet_loss_volte REAL,

            voice_traffic_volte_erlang REAL,


            /* ================================================
               AUDIT
               ================================================ */

            source_file TEXT,

            uploaded_at TEXT NOT NULL,


            /* ================================================
               DUPLICATE PROTECTION
               ================================================ */

            UNIQUE (
                time,
                ihs_id
            )
        )
        """
    )


    # ========================================================
    # UPLOAD HISTORY
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS upload_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            uploaded_at TEXT NOT NULL,

            total_rows INTEGER DEFAULT 0,

            inserted_rows INTEGER DEFAULT 0,

            duplicate_rows INTEGER DEFAULT 0,

            rejected_rows INTEGER DEFAULT 0,

            earliest_date TEXT,

            latest_date TEXT,

            status TEXT
        )
        """
    )


    # ========================================================
    # INDEXES
    # ========================================================

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_daily_kpi_time
        ON daily_kpi(time)
        """
    )


    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_daily_kpi_ihs
        ON daily_kpi(ihs_id)
        """
    )


    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_daily_kpi_bts
        ON daily_kpi(bts_2g)
        """
    )


    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_daily_kpi_vendor
        ON daily_kpi(vendor)
        """
    )


    connection.commit()

    connection.close()


# ============================================================
# TEMPLATE VALIDATION
# ============================================================

def validate_template(
    dataframe
):

    dataframe_columns = list(
        dataframe.columns
    )


    missing_identifiers = [

        column

        for column
        in REQUIRED_IDENTIFIER_COLUMNS

        if column
        not in dataframe_columns
    ]


    missing_template_columns = [

        column

        for column
        in MASTER_TEMPLATE_COLUMNS

        if column
        not in dataframe_columns
    ]


    extra_columns = [

        column

        for column
        in dataframe_columns

        if column
        not in MASTER_TEMPLATE_COLUMNS
    ]


    return {

        "valid_identifiers":
            len(
                missing_identifiers
            )
            ==
            0,

        "valid_full_template":
            len(
                missing_template_columns
            )
            ==
            0,

        "missing_identifiers":
            missing_identifiers,

        "missing_columns":
            missing_template_columns,

        "extra_columns":
            extra_columns,

        "expected_columns":
            len(
                MASTER_TEMPLATE_COLUMNS
            ),

        "received_columns":
            len(
                dataframe_columns
            )
    }


# ============================================================
# CLEAN UPLOADED DATAFRAME
# ============================================================

def clean_uploaded_dataframe(
    dataframe
):

    df = dataframe.copy()


    # ========================================================
    # REMOVE COMPLETELY EMPTY ROWS
    # ========================================================

    df = df.dropna(
        how="all"
    )


    # ========================================================
    # RECOGNIZED COLUMNS ONLY
    # ========================================================

    recognized_columns = [

        column

        for column
        in MASTER_TEMPLATE_COLUMNS

        if column
        in df.columns
    ]


    df = df[
        recognized_columns
    ].copy()


    # ========================================================
    # DATABASE COLUMN NAMES
    # ========================================================

    df = df.rename(
        columns=COLUMN_MAP
    )


    # ========================================================
    # DATE
    # ========================================================

    if "time" in df.columns:

        df[
            "time"
        ] = pd.to_datetime(
            df[
                "time"
            ],
            errors="coerce"
        )


        df[
            "time"
        ] = (
            df[
                "time"
            ]
            .dt
            .normalize()
        )


    # ========================================================
    # TEXT COLUMNS
    # ========================================================

    for column in [
        "bts_2g",
        "ihs_id",
        "vendor"
    ]:

        if column in df.columns:

            df[
                column
            ] = (
                df[
                    column
                ]
                .astype(
                    "string"
                )
                .str
                .strip()
            )


    # ========================================================
    # NUMERIC COLUMNS
    # ========================================================

    text_columns = {
        "time",
        "bts_2g",
        "ihs_id",
        "vendor"
    }


    numeric_columns = [

        column

        for column
        in df.columns

        if column
        not in text_columns
    ]


    for column in numeric_columns:

        df[
            column
        ] = pd.to_numeric(
            df[
                column
            ],
            errors="coerce"
        )


    # ========================================================
    # REMOVE INVALID DATABASE KEYS
    # ========================================================

    if (
        "time" in df.columns
        and
        "ihs_id" in df.columns
    ):

        df = df.dropna(
            subset=[
                "time",
                "ihs_id"
            ]
        )


    if "ihs_id" in df.columns:

        df = df[
            df[
                "ihs_id"
            ]
            .astype(str)
            .str
            .strip()
            !=
            ""
        ]


    # ========================================================
    # DATE TO DATABASE STRING
    # ========================================================

    if "time" in df.columns:

        df[
            "time"
        ] = (
            df[
                "time"
            ]
            .dt
            .strftime(
                "%Y-%m-%d"
            )
        )


    return df.reset_index(
        drop=True
    )


# ============================================================
# PROFILE DATAFRAME
# ============================================================

def profile_dataframe(
    dataframe
):

    df = dataframe.copy()


    # ========================================================
    # DATES
    # ========================================================

    if "Time" in df.columns:

        dates = pd.to_datetime(
            df[
                "Time"
            ],
            errors="coerce"
        )


        earliest = (
            dates.min()
        )


        latest = (
            dates.max()
        )


        reporting_days = (
            dates
            .dt
            .normalize()
            .nunique()
        )

    else:

        earliest = None

        latest = None

        reporting_days = 0


    # ========================================================
    # SITES
    # ========================================================

    if "IHS ID" in df.columns:

        sites = (
            df[
                "IHS ID"
            ]
            .dropna()
            .astype(str)
            .nunique()
        )

    else:

        sites = 0


    # ========================================================
    # VENDORS
    # ========================================================

    if "Vendor" in df.columns:

        vendors = sorted(
            df[
                "Vendor"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    else:

        vendors = []


    return {

        "rows":
            len(
                df
            ),

        "sites":
            int(
                sites
            ),

        "reporting_days":
            int(
                reporting_days
            ),

        "earliest_date":
            earliest,

        "latest_date":
            latest,

        "vendors":
            vendors
    }


# ============================================================
# INSERT KPI DATAFRAME
# ============================================================

def insert_kpi_dataframe(
    dataframe,
    filename="uploaded_file"
):

    initialize_database()


    original_rows = len(
        dataframe
    )


    cleaned_df = (
        clean_uploaded_dataframe(
            dataframe
        )
    )


    cleaned_rows = len(
        cleaned_df
    )


    rejected_rows = (
        original_rows
        -
        cleaned_rows
    )


    if cleaned_df.empty:

        return {

            "success":
                False,

            "total_rows":
                original_rows,

            "inserted_rows":
                0,

            "duplicate_rows":
                0,

            "rejected_rows":
                rejected_rows,

            "message":
                "No valid KPI rows were found."
        }


    connection = get_connection()

    cursor = connection.cursor()


    uploaded_at = (
        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    database_columns = list(
        COLUMN_MAP.values()
    )


    # ========================================================
    # ADD ANY MISSING TEMPLATE FIELDS AS NULL
    # ========================================================

    for column in database_columns:

        if column not in cleaned_df.columns:

            cleaned_df[
                column
            ] = np.nan


    cleaned_df = cleaned_df[
        database_columns
    ]


    inserted_rows = 0

    duplicate_rows = 0


    # ========================================================
    # INSERT SQL
    # ========================================================

    insert_columns = (
        database_columns
        +
        [
            "source_file",
            "uploaded_at"
        ]
    )


    placeholders = ",".join(
        [
            "?"
        ]
        *
        len(
            insert_columns
        )
    )


    column_sql = ",".join(
        insert_columns
    )


    insert_sql = f"""
        INSERT OR IGNORE INTO daily_kpi
        (
            {column_sql}
        )
        VALUES
        (
            {placeholders}
        )
    """


    # ========================================================
    # INSERT RECORDS
    # ========================================================

    for _, row in cleaned_df.iterrows():

        values = []


        for column in database_columns:

            value = row[
                column
            ]


            if pd.isna(
                value
            ):

                values.append(
                    None
                )


            elif isinstance(
                value,
                np.generic
            ):

                values.append(
                    value.item()
                )


            else:

                values.append(
                    value
                )


        values.extend(
            [
                filename,
                uploaded_at
            ]
        )


        cursor.execute(
            insert_sql,
            values
        )


        if cursor.rowcount == 1:

            inserted_rows += 1

        else:

            duplicate_rows += 1


    # ========================================================
    # DATE RANGE
    # ========================================================

    valid_dates = pd.to_datetime(
        cleaned_df[
            "time"
        ],
        errors="coerce"
    )


    earliest_date = (
        valid_dates.min()
    )


    latest_date = (
        valid_dates.max()
    )


    earliest_date_string = (

        earliest_date
        .strftime(
            "%Y-%m-%d"
        )

        if pd.notna(
            earliest_date
        )

        else None
    )


    latest_date_string = (

        latest_date
        .strftime(
            "%Y-%m-%d"
        )

        if pd.notna(
            latest_date
        )

        else None
    )


    # ========================================================
    # UPLOAD HISTORY
    # ========================================================

    status = (

        "SUCCESS"

        if inserted_rows > 0

        else "DUPLICATE"
    )


    cursor.execute(
        """
        INSERT INTO upload_history
        (
            filename,
            uploaded_at,
            total_rows,
            inserted_rows,
            duplicate_rows,
            rejected_rows,
            earliest_date,
            latest_date,
            status
        )

        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,

        (
            filename,
            uploaded_at,
            original_rows,
            inserted_rows,
            duplicate_rows,
            rejected_rows,
            earliest_date_string,
            latest_date_string,
            status
        )
    )


    connection.commit()

    connection.close()


    return {

        "success":
            True,

        "total_rows":
            original_rows,

        "clean_rows":
            cleaned_rows,

        "inserted_rows":
            inserted_rows,

        "duplicate_rows":
            duplicate_rows,

        "rejected_rows":
            rejected_rows,

        "earliest_date":
            earliest_date_string,

        "latest_date":
            latest_date_string,

        "message":
            (
                f"{inserted_rows:,} record(s) added. "
                f"{duplicate_rows:,} duplicate(s) skipped."
            )
    }


# ============================================================
# DATABASE HAS DATA
# ============================================================

def database_has_data():

    initialize_database()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_kpi
        """
    )


    count = cursor.fetchone()[
        0
    ]


    connection.close()


    return count > 0


# ============================================================
# GET ALL KPI DATA
# ============================================================

def get_all_kpi_data():

    initialize_database()


    connection = get_connection()


    dataframe = pd.read_sql_query(
        """
        SELECT *

        FROM daily_kpi

        ORDER BY
            time ASC,
            ihs_id ASC
        """,
        connection
    )


    connection.close()


    if (
        not dataframe.empty
        and
        "time" in dataframe.columns
    ):

        dataframe[
            "time"
        ] = pd.to_datetime(
            dataframe[
                "time"
            ],
            errors="coerce"
        )


    return dataframe


# ============================================================
# GET DATA BY DATE
# ============================================================

def get_kpi_data_by_date(
    start_date=None,
    end_date=None
):

    initialize_database()


    connection = get_connection()


    query = """

        SELECT *

        FROM daily_kpi

        WHERE 1 = 1

    """


    parameters = []


    if start_date is not None:

        query += """

            AND time >= ?

        """

        parameters.append(
            pd.to_datetime(
                start_date
            )
            .strftime(
                "%Y-%m-%d"
            )
        )


    if end_date is not None:

        query += """

            AND time <= ?

        """

        parameters.append(
            pd.to_datetime(
                end_date
            )
            .strftime(
                "%Y-%m-%d"
            )
        )


    query += """

        ORDER BY
            time ASC,
            ihs_id ASC

    """


    dataframe = pd.read_sql_query(
        query,
        connection,
        params=parameters
    )


    connection.close()


    if (
        not dataframe.empty
        and
        "time" in dataframe.columns
    ):

        dataframe[
            "time"
        ] = pd.to_datetime(
            dataframe[
                "time"
            ],
            errors="coerce"
        )


    return dataframe


# ============================================================
# GET LATEST KPI DATE
# ============================================================

def get_latest_kpi_date():

    initialize_database()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT MAX(time)
        FROM daily_kpi
        """
    )


    result = cursor.fetchone()[
        0
    ]


    connection.close()


    if result is None:

        return None


    return pd.to_datetime(
        result
    )


# ============================================================
# GET EARLIEST KPI DATE
# ============================================================

def get_earliest_kpi_date():

    initialize_database()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT MIN(time)
        FROM daily_kpi
        """
    )


    result = cursor.fetchone()[
        0
    ]


    connection.close()


    if result is None:

        return None


    return pd.to_datetime(
        result
    )


# ============================================================
# GET LATEST DAY DATA
# ============================================================

def get_latest_day_data():

    latest_date = (
        get_latest_kpi_date()
    )


    if latest_date is None:

        return pd.DataFrame()


    return get_kpi_data_by_date(
        latest_date,
        latest_date
    )


# ============================================================
# GET TECHNOLOGY DATA
# ============================================================

def get_technology_data(
    technology,
    start_date=None,
    end_date=None
):

    technology = (
        str(
            technology
        )
        .strip()
    )


    if technology not in TECHNOLOGY_COLUMNS:

        raise ValueError(
            (
                "Technology must be one of "
                "2G, 3G, 4G, 5G or VoLTE."
            )
        )


    dataframe = get_kpi_data_by_date(
        start_date=start_date,
        end_date=end_date
    )


    if dataframe.empty:

        return dataframe


    selected_columns = [

        column

        for column
        in TECHNOLOGY_COLUMNS[
            technology
        ]

        if column
        in dataframe.columns
    ]


    return dataframe[
        selected_columns
    ].copy()


# ============================================================
# GET SITE DATA
# ============================================================

def get_site_data(
    ihs_id=None,
    bts=None,
    start_date=None,
    end_date=None
):

    dataframe = get_kpi_data_by_date(
        start_date=start_date,
        end_date=end_date
    )


    if dataframe.empty:

        return dataframe


    if ihs_id is not None:

        dataframe = dataframe[
            dataframe[
                "ihs_id"
            ]
            .astype(str)
            ==
            str(
                ihs_id
            )
        ]


    if bts is not None:

        dataframe = dataframe[
            dataframe[
                "bts_2g"
            ]
            .astype(str)
            ==
            str(
                bts
            )
        ]


    return dataframe.reset_index(
        drop=True
    )


# ============================================================
# GET SITE LIST
# ============================================================

def get_site_list():

    initialize_database()


    connection = get_connection()


    dataframe = pd.read_sql_query(
        """
        SELECT DISTINCT

            ihs_id,
            bts_2g,
            vendor

        FROM daily_kpi

        WHERE ihs_id IS NOT NULL

        ORDER BY ihs_id
        """,
        connection
    )


    connection.close()


    return dataframe


# ============================================================
# GET VENDOR LIST
# ============================================================

def get_vendor_list():

    initialize_database()


    connection = get_connection()


    dataframe = pd.read_sql_query(
        """
        SELECT DISTINCT vendor

        FROM daily_kpi

        WHERE vendor IS NOT NULL

        ORDER BY vendor
        """,
        connection
    )


    connection.close()


    if dataframe.empty:

        return []


    return (
        dataframe[
            "vendor"
        ]
        .dropna()
        .astype(str)
        .tolist()
    )


# ============================================================
# DATABASE SUMMARY
# ============================================================

def get_database_summary():

    initialize_database()


    connection = get_connection()

    cursor = connection.cursor()


    # ========================================================
    # TOTAL RECORDS
    # ========================================================

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_kpi
        """
    )


    total_records = cursor.fetchone()[
        0
    ]


    # ========================================================
    # SITES
    # ========================================================

    cursor.execute(
        """
        SELECT COUNT(
            DISTINCT ihs_id
        )

        FROM daily_kpi
        """
    )


    total_sites = cursor.fetchone()[
        0
    ]


    # ========================================================
    # REPORTING DAYS
    # ========================================================

    cursor.execute(
        """
        SELECT COUNT(
            DISTINCT time
        )

        FROM daily_kpi
        """
    )


    reporting_days = cursor.fetchone()[
        0
    ]


    # ========================================================
    # VENDORS
    # ========================================================

    cursor.execute(
        """
        SELECT COUNT(
            DISTINCT vendor
        )

        FROM daily_kpi

        WHERE vendor IS NOT NULL
        """
    )


    total_vendors = cursor.fetchone()[
        0
    ]


    # ========================================================
    # DATE RANGE
    # ========================================================

    cursor.execute(
        """
        SELECT

            MIN(time),
            MAX(time)

        FROM daily_kpi
        """
    )


    date_result = (
        cursor.fetchone()
    )


    earliest_date = (
        date_result[
            0
        ]
    )


    latest_date = (
        date_result[
            1
        ]
    )


    connection.close()


    return {

        "total_records":
            int(
                total_records
            ),

        "total_sites":
            int(
                total_sites
            ),

        "reporting_days":
            int(
                reporting_days
            ),

        "total_vendors":
            int(
                total_vendors
            ),

        "earliest_date":
            earliest_date,

        "latest_date":
            latest_date
    }


# ============================================================
# GET UPLOAD HISTORY
# ============================================================

def get_upload_history(
    limit=20
):

    initialize_database()


    connection = get_connection()


    dataframe = pd.read_sql_query(
        """
        SELECT

            filename,
            uploaded_at,
            total_rows,
            inserted_rows,
            duplicate_rows,
            rejected_rows,
            earliest_date,
            latest_date,
            status

        FROM upload_history

        ORDER BY id DESC

        LIMIT ?
        """,

        connection,

        params=[
            int(
                limit
            )
        ]
    )


    connection.close()


    return dataframe


# ============================================================
# LATEST NETWORK KPI SUMMARY
# ============================================================

def get_latest_network_summary():

    dataframe = (
        get_latest_day_data()
    )


    if dataframe.empty:

        return {}


    # ========================================================
    # AVAILABILITY BY TECHNOLOGY
    # ========================================================

    availability_2g = safe_numeric_mean(
        dataframe,
        "availability_2g"
    )


    availability_3g = safe_numeric_mean(
        dataframe,
        "availability_3g"
    )


    availability_4g = safe_numeric_mean(
        dataframe,
        "availability_4g"
    )


    availability_5g = safe_numeric_mean(
        dataframe,
        "availability_5g"
    )


    availability_volte = safe_numeric_mean(
        dataframe,
        "availability_volte"
    )


    availability_values = [

        value

        for value in [

            availability_2g,
            availability_3g,
            availability_4g,
            availability_5g,
            availability_volte

        ]

        if pd.notna(
            value
        )
    ]


    overall_availability = (

        float(
            np.mean(
                availability_values
            )
        )

        if availability_values

        else np.nan
    )


    # ========================================================
    # DATA TRAFFIC
    # ========================================================

    data_2g = safe_numeric_sum(
        dataframe,
        "data_2g_mb"
    )


    data_3g = safe_numeric_sum(
        dataframe,
        "data_3g_mb"
    )


    data_4g = safe_numeric_sum(
        dataframe,
        "data_4g_mb"
    )


    data_5g = safe_numeric_sum(
        dataframe,
        "data_5g_mb"
    )


    data_values = [

        value

        for value in [

            data_2g,
            data_3g,
            data_4g,
            data_5g

        ]

        if pd.notna(
            value
        )
    ]


    total_data_mb = (

        float(
            np.sum(
                data_values
            )
        )

        if data_values

        else np.nan
    )


    # ========================================================
    # VOICE TRAFFIC
    # ========================================================

    voice_2g = safe_numeric_sum(
        dataframe,
        "tch_erlang_2g"
    )


    voice_3g = safe_numeric_sum(
        dataframe,
        "erlang_3g"
    )


    voice_volte = safe_numeric_sum(
        dataframe,
        "voice_traffic_volte_erlang"
    )


    voice_values = [

        value

        for value in [

            voice_2g,
            voice_3g,
            voice_volte

        ]

        if pd.notna(
            value
        )
    ]


    total_voice_erlang = (

        float(
            np.sum(
                voice_values
            )
        )

        if voice_values

        else np.nan
    )


    # ========================================================
    # ACCESSIBILITY
    # ========================================================

    accessibility_values = []


    for column in [

        "cssr_2g",
        "cssr_3g",
        "rrc_success_4g",
        "rrc_success_5g",
        "cssr_volte"

    ]:

        value = safe_numeric_mean(
            dataframe,
            column
        )


        if pd.notna(
            value
        ):

            accessibility_values.append(
                value
            )


    accessibility = (

        float(
            np.mean(
                accessibility_values
            )
        )

        if accessibility_values

        else np.nan
    )


    # ========================================================
    # MOBILITY / HOSR
    # ========================================================

    mobility_values = []


    for column in [

        "hosr_3g",
        "hosr_4g",
        "hosr_5g",
        "hosr_volte"

    ]:

        value = safe_numeric_mean(
            dataframe,
            column
        )


        if pd.notna(
            value
        ):

            mobility_values.append(
                value
            )


    overall_hosr = (

        float(
            np.mean(
                mobility_values
            )
        )

        if mobility_values

        else np.nan
    )


    # ========================================================
    # DROP RATE
    # ========================================================

    drop_values = []


    for column in [

        "drop_call_rate_2g",
        "dcr_volte"

    ]:

        value = safe_numeric_mean(
            dataframe,
            column
        )


        if pd.notna(
            value
        ):

            drop_values.append(
                value
            )


    overall_drop_rate = (

        float(
            np.mean(
                drop_values
            )
        )

        if drop_values

        else np.nan
    )


    # ========================================================
    # RETURN SUMMARY
    # ========================================================

    return {

        "latest_date":
            dataframe[
                "time"
            ].max(),

        "records":
            len(
                dataframe
            ),

        "sites":
            dataframe[
                "ihs_id"
            ]
            .nunique(),

        "vendors":
            dataframe[
                "vendor"
            ]
            .nunique(),

        "network_availability":
            overall_availability,

        "total_data_mb":
            total_data_mb,

        "total_data_gb":
            (
                total_data_mb
                /
                1024

                if pd.notna(
                    total_data_mb
                )

                else np.nan
            ),

        "total_data_tb":
            (
                total_data_mb
                /
                1024
                /
                1024

                if pd.notna(
                    total_data_mb
                )

                else np.nan
            ),

        "total_voice_erlang":
            total_voice_erlang,

        "accessibility":
            accessibility,

        "drop_rate":
            overall_drop_rate,

        "hosr":
            overall_hosr,

        "availability_2g":
            availability_2g,

        "availability_3g":
            availability_3g,

        "availability_4g":
            availability_4g,

        "availability_5g":
            availability_5g,

        "availability_volte":
            availability_volte
    }


# ============================================================
# TECHNOLOGY HEALTH
# ============================================================

def get_latest_technology_health():

    dataframe = (
        get_latest_day_data()
    )


    if dataframe.empty:

        return pd.DataFrame()


    health_rows = []


    # ========================================================
    # 2G
    # ========================================================

    health_rows.append(
        {

            "Technology":
                "2G",

            "Availability":
                safe_numeric_mean(
                    dataframe,
                    "availability_2g"
                ),

            "Accessibility":
                safe_numeric_mean(
                    dataframe,
                    "cssr_2g"
                ),

            "Retainability":
                safe_numeric_mean(
                    dataframe,
                    "drop_call_rate_2g"
                ),

            "Mobility":
                np.nan,

            "Traffic":
                safe_numeric_sum(
                    dataframe,
                    "tch_erlang_2g"
                )
        }
    )


    # ========================================================
    # 3G
    # ========================================================

    health_rows.append(
        {

            "Technology":
                "3G",

            "Availability":
                safe_numeric_mean(
                    dataframe,
                    "availability_3g"
                ),

            "Accessibility":
                safe_numeric_mean(
                    dataframe,
                    "cssr_3g"
                ),

            "Retainability":
                np.nan,

            "Mobility":
                safe_numeric_mean(
                    dataframe,
                    "hosr_3g"
                ),

            "Traffic":
                safe_numeric_sum(
                    dataframe,
                    "data_3g_mb"
                )
        }
    )


    # ========================================================
    # 4G
    # ========================================================

    health_rows.append(
        {

            "Technology":
                "4G",

            "Availability":
                safe_numeric_mean(
                    dataframe,
                    "availability_4g"
                ),

            "Accessibility":
                safe_numeric_mean(
                    dataframe,
                    "rrc_success_4g"
                ),

            "Retainability":
                safe_numeric_mean(
                    dataframe,
                    "erab_success_4g"
                ),

            "Mobility":
                safe_numeric_mean(
                    dataframe,
                    "hosr_4g"
                ),

            "Traffic":
                safe_numeric_sum(
                    dataframe,
                    "data_4g_mb"
                )
        }
    )


    # ========================================================
    # 5G
    # ========================================================

    health_rows.append(
        {

            "Technology":
                "5G",

            "Availability":
                safe_numeric_mean(
                    dataframe,
                    "availability_5g"
                ),

            "Accessibility":
                safe_numeric_mean(
                    dataframe,
                    "rrc_success_5g"
                ),

            "Retainability":
                safe_numeric_mean(
                    dataframe,
                    "pdu_session_success_5g"
                ),

            "Mobility":
                safe_numeric_mean(
                    dataframe,
                    "hosr_5g"
                ),

            "Traffic":
                safe_numeric_sum(
                    dataframe,
                    "data_5g_mb"
                )
        }
    )


    # ========================================================
    # VoLTE
    # ========================================================

    health_rows.append(
        {

            "Technology":
                "VoLTE",

            "Availability":
                safe_numeric_mean(
                    dataframe,
                    "availability_volte"
                ),

            "Accessibility":
                safe_numeric_mean(
                    dataframe,
                    "cssr_volte"
                ),

            "Retainability":
                safe_numeric_mean(
                    dataframe,
                    "dcr_volte"
                ),

            "Mobility":
                safe_numeric_mean(
                    dataframe,
                    "hosr_volte"
                ),

            "Traffic":
                safe_numeric_sum(
                    dataframe,
                    "voice_traffic_volte_erlang"
                )
        }
    )


    return pd.DataFrame(
        health_rows
    )


# ============================================================
# WORST PERFORMING SITES
# ============================================================

def get_worst_sites(
    limit=10
):

    dataframe = (
        get_latest_day_data()
    )


    if dataframe.empty:

        return pd.DataFrame()


    df = dataframe.copy()


    # ========================================================
    # AVERAGE AVAILABILITY
    # ========================================================

    availability_columns = [

        "availability_2g",
        "availability_3g",
        "availability_4g",
        "availability_5g",
        "availability_volte"
    ]


    availability_data = []


    for column in availability_columns:

        if column in df.columns:

            availability_data.append(
                pd.to_numeric(
                    df[
                        column
                    ],
                    errors="coerce"
                )
            )


    if availability_data:

        availability_frame = pd.concat(
            availability_data,
            axis=1
        )


        df[
            "average_availability"
        ] = availability_frame.mean(
            axis=1,
            skipna=True
        )


    else:

        df[
            "average_availability"
        ] = np.nan


    # ========================================================
    # PENALTIES
    # ========================================================

    df[
        "drop_penalty"
    ] = pd.to_numeric(
        df[
            "drop_call_rate_2g"
        ],
        errors="coerce"
    ).fillna(
        0
    )


    df[
        "volte_drop_penalty"
    ] = pd.to_numeric(
        df[
            "dcr_volte"
        ],
        errors="coerce"
    ).fillna(
        0
    )


    df[
        "tch_congestion_penalty"
    ] = pd.to_numeric(
        df[
            "tch_congestion_2g"
        ],
        errors="coerce"
    ).fillna(
        0
    )


    # ========================================================
    # HEALTH SCORE
    # ========================================================

    df[
        "health_score"
    ] = (

        df[
            "average_availability"
        ]

        -

        df[
            "drop_penalty"
        ]

        -

        df[
            "volte_drop_penalty"
        ]

        -

        (
            df[
                "tch_congestion_penalty"
            ]
            *
            0.25
        )
    )


    worst = (
        df
        .sort_values(
            "health_score",
            ascending=True,
            na_position="last"
        )
        .head(
            int(
                limit
            )
        )
    )


    return worst[
        [

            "ihs_id",
            "bts_2g",
            "vendor",

            "average_availability",

            "drop_call_rate_2g",

            "tch_congestion_2g",

            "dcr_volte",

            "health_score"
        ]
    ].reset_index(
        drop=True
    )


# ============================================================
# CLEAR DATABASE
# ============================================================

def clear_database():

    initialize_database()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM daily_kpi
        """
    )


    cursor.execute(
        """
        DELETE FROM upload_history
        """
    )


    connection.commit()

    connection.close()


# ============================================================
# INITIALIZE WHEN IMPORTED
# ============================================================

initialize_database()