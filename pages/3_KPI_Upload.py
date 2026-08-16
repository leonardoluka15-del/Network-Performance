import streamlit as st
import pandas as pd

from io import BytesIO

from navigation import navigation

from data.database import (
    validate_template,
    profile_dataframe,
    insert_kpi_dataframe,
    get_database_summary,
    get_upload_history
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="KPI Upload - Network Operations",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HEADER / NAVIGATION
# ============================================================

navigation("KPI Upload")


# ============================================================
# PAGE CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PAGE WRAPPER
   ========================================================= */

.upload-wrapper {
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

.upload-title {
    font-size: 28px;
    font-weight: 700;
    color: #111111;
    margin: 0;
}

.upload-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
    margin-bottom: 18px;
}


/* =========================================================
   PANELS
   ========================================================= */

div[class*="st-key-upload_panel_"],
div[class*="st-key-upload_kpi_"] {

    border: 2px solid #8f969f !important;

    border-radius: 8px !important;

    background-color: #ffffff !important;

    box-sizing: border-box !important;

    box-shadow: none !important;
}


/* =========================================================
   REMOVE INTERNAL BORDER
   ========================================================= */

div[class*="st-key-upload_panel_"]
div[data-testid="stVerticalBlockBorderWrapper"],

div[class*="st-key-upload_kpi_"]
div[data-testid="stVerticalBlockBorderWrapper"] {

    border: none !important;

    box-shadow: none !important;
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
   KPI
   ========================================================= */

.upload-kpi-title {
    font-size: 12px;
    color: #6b7280;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.upload-kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #181818;
    margin-bottom: 6px;
    line-height: 1.15;
}

.upload-kpi-note {
    color: #6b7280;
    font-size: 11px;
    font-weight: 600;
}


/* =========================================================
   VALIDATION STATUS
   ========================================================= */

.validation-ok {
    color: #15803d;
    font-weight: 700;
    font-size: 13px;
}

.validation-warning {
    color: #b45309;
    font-weight: 700;
    font-size: 13px;
}

.validation-error {
    color: #b91c1c;
    font-weight: 700;
    font-size: 13px;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed #8f969f !important;
    border-radius: 8px !important;
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
# HELPERS
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


def upload_kpi_card(
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
                f'<div class="upload-kpi-title">'
                f'{title}'
                f'</div>'
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            (
                f'<div class="upload-kpi-value">'
                f'{value}'
                f'</div>'
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            (
                f'<div class="upload-kpi-note">'
                f'{note}'
                f'</div>'
            ),
            unsafe_allow_html=True
        )


def read_uploaded_file(
    uploaded_file
):

    filename = uploaded_file.name.lower()


    if filename.endswith(
        ".xlsx"
    ):

        dataframe = pd.read_excel(
            uploaded_file,
            engine="openpyxl"
        )


    elif filename.endswith(
        ".csv"
    ):

        dataframe = pd.read_csv(
            uploaded_file
        )


    else:

        raise ValueError(
            "Unsupported file type."
        )


    return dataframe


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    (
        '<div class="upload-wrapper">'
        '<div class="upload-title">'
        'KPI Data Upload'
        '</div>'
        '<div class="upload-subtitle">'
        'Validate and add daily 2G, 3G, 4G, 5G and VoLTE KPI records to the network database'
        '</div>'
        '</div>'
    ),
    unsafe_allow_html=True
)


# ============================================================
# DATABASE STATUS
# ============================================================

database_summary = (
    get_database_summary()
)


with st.container(
    border=True,
    key="upload_panel_database_status"
):

    panel_title(
        "Database Status",
        "Current KPI database information"
    )


    db1, db2, db3, db4 = (
        st.columns(
            4,
            gap="small"
        )
    )


    with db1:

        upload_kpi_card(
            "Database Records",
            f"{database_summary['total_records']:,}",
            "Stored KPI records",
            "upload_kpi_database_records"
        )


    with db2:

        upload_kpi_card(
            "Sites",
            f"{database_summary['total_sites']:,}",
            "Unique IHS sites",
            "upload_kpi_database_sites"
        )


    with db3:

        upload_kpi_card(
            "Reporting Days",
            f"{database_summary['reporting_days']:,}",
            "Unique KPI dates",
            "upload_kpi_database_days"
        )


    with db4:

        latest_db_date = (
            database_summary[
                "latest_date"
            ]
        )


        upload_kpi_card(
            "Latest KPI Date",
            (
                latest_db_date
                if latest_db_date
                else "—"
            ),
            "Most recent stored KPI date",
            "upload_kpi_database_latest"
        )


# ============================================================
# MASTER TEMPLATE INFORMATION
# ============================================================

st.write("")


with st.container(
    border=True,
    key="upload_panel_template"
):

    panel_title(
        "Master KPI Template",
        (
            "Daily KPI uploads must follow the approved "
            "2G / 3G / 4G / 5G / VoLTE column structure"
        )
    )


    st.markdown(
        """
The upload template contains:

**General identification**

- Time, 2G BTS, IHS ID, Vendor

**Technology KPI groups**

- 2G, 3G, 4G, 5G, VoLTE

Do not rename the column headers. KPI values may be blank when a technology is not deployed at a site.
"""
    )


# ============================================================
# FILE UPLOAD
# ============================================================

st.write("")


with st.container(
    border=True,
    key="upload_panel_file"
):

    panel_title(
        "Upload Daily KPI File",
        "Supported formats: XLSX and CSV"
    )


    uploaded_file = st.file_uploader(
        "Upload KPI File",
        type=[
            "xlsx",
            "csv"
        ],
        label_visibility="collapsed",
        key="master_kpi_upload"
    )


# ============================================================
# NO FILE YET
# ============================================================

if uploaded_file is None:

    st.info(
        (
            "Upload a completed KPI master-template file "
            "to begin validation."
        )
    )


# ============================================================
# PROCESS UPLOADED FILE
# ============================================================

else:

    try:

        uploaded_df = (
            read_uploaded_file(
                uploaded_file
            )
        )


    except Exception as error:

        st.error(
            (
                "The uploaded file could not be read.\n\n"
                f"{error}"
            )
        )

        st.stop()


    # ========================================================
    # BASIC FILE PROFILE
    # ========================================================

    file_profile = (
        profile_dataframe(
            uploaded_df
        )
    )


    # ========================================================
    # TEMPLATE VALIDATION
    # ========================================================

    validation = (
        validate_template(
            uploaded_df
        )
    )


    # ========================================================
    # FILE SUMMARY
    # ========================================================

    st.write("")


    with st.container(
        border=True,
        key="upload_panel_file_summary"
    ):

        panel_title(
            "Uploaded File Summary",
            uploaded_file.name
        )


        summary1, summary2, summary3, summary4 = (
            st.columns(
                4,
                gap="small"
            )
        )


        with summary1:

            upload_kpi_card(
                "Rows",
                f"{file_profile['rows']:,}",
                "Records found",
                "upload_kpi_file_rows"
            )


        with summary2:

            upload_kpi_card(
                "Sites",
                f"{file_profile['sites']:,}",
                "Unique IHS IDs",
                "upload_kpi_file_sites"
            )


        with summary3:

            upload_kpi_card(
                "Reporting Days",
                f"{file_profile['reporting_days']:,}",
                "Unique KPI dates",
                "upload_kpi_file_days"
            )


        with summary4:

            upload_kpi_card(
                "Vendors",
                f"{len(file_profile['vendors']):,}",
                (
                    ", ".join(
                        file_profile[
                            "vendors"
                        ]
                    )
                    if file_profile[
                        "vendors"
                    ]
                    else "No vendor values"
                ),
                "upload_kpi_file_vendors"
            )


    # ========================================================
    # DATE SUMMARY
    # ========================================================

    earliest_date = (
        file_profile[
            "earliest_date"
        ]
    )


    latest_date = (
        file_profile[
            "latest_date"
        ]
    )


    if pd.notna(
        earliest_date
    ):

        earliest_date_text = (
            pd.to_datetime(
                earliest_date
            )
            .strftime(
                "%d %b %Y"
            )
        )

    else:

        earliest_date_text = "—"


    if pd.notna(
        latest_date
    ):

        latest_date_text = (
            pd.to_datetime(
                latest_date
            )
            .strftime(
                "%d %b %Y"
            )
        )

    else:

        latest_date_text = "—"


    st.caption(
        (
            f"Reporting period: "
            f"{earliest_date_text} "
            f"to "
            f"{latest_date_text}"
        )
    )


    # ========================================================
    # VALIDATION PANEL
    # ========================================================

    st.write("")


    with st.container(
        border=True,
        key="upload_panel_validation"
    ):

        panel_title(
            "File Validation",
            "Template and structural validation before database insertion"
        )


        # ====================================================
        # IDENTIFIER VALIDATION
        # ====================================================

        if validation[
            "valid_identifiers"
        ]:

            st.markdown(
                (
                    '<div class="validation-ok">'
                    '✓ Required identification columns found'
                    '</div>'
                ),
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                (
                    '<div class="validation-error">'
                    '✗ Required identification columns are missing'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


            st.error(
                (
                    "Missing required columns:\n\n"
                    +
                    "\n".join(
                        [
                            f"- {column}"
                            for column
                            in validation[
                                "missing_identifiers"
                            ]
                        ]
                    )
                )
            )


        # ====================================================
        # FULL MASTER TEMPLATE
        # ====================================================

        if validation[
            "valid_full_template"
        ]:

            st.markdown(
                (
                    '<div class="validation-ok">'
                    '✓ Full master KPI template detected'
                    '</div>'
                ),
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                (
                    '<div class="validation-warning">'
                    '⚠ Some master KPI columns are missing'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


            if validation[
                "missing_columns"
            ]:

                with st.expander(
                    (
                        "View missing KPI columns "
                        f"({len(validation['missing_columns'])})"
                    )
                ):

                    for column in validation[
                        "missing_columns"
                    ]:

                        st.write(
                            f"• {column}"
                        )


        # ====================================================
        # EXTRA COLUMNS
        # ====================================================

        if validation[
            "extra_columns"
        ]:

            st.markdown(
                (
                    '<div class="validation-warning">'
                    '⚠ Additional columns detected'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


            with st.expander(
                (
                    "View additional columns "
                    f"({len(validation['extra_columns'])})"
                )
            ):

                for column in validation[
                    "extra_columns"
                ]:

                    st.write(
                        f"• {column}"
                    )


        else:

            st.markdown(
                (
                    '<div class="validation-ok">'
                    '✓ No unexpected columns detected'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


        st.write("")


        structure1, structure2 = (
            st.columns(
                2
            )
        )


        with structure1:

            st.metric(
                "Expected Columns",
                validation[
                    "expected_columns"
                ]
            )


        with structure2:

            st.metric(
                "Received Columns",
                validation[
                    "received_columns"
                ]
            )


    # ========================================================
    # TECHNOLOGY PRESENCE
    # ========================================================

    st.write("")


    with st.container(
        border=True,
        key="upload_panel_technology"
    ):

        panel_title(
            "Technology KPI Coverage",
            "Detected technology groups in the uploaded file"
        )


        technology_groups = {

            "2G": [
                "2G AVAIL(%)",
                "2G Call Setup Success Rate (CS)_MTN(%)"
            ],

            "3G": [
                "3G Call Setup Success Rate (CS)_MTN(%)",
                "Availability Rate (Cell)_MTN(%)"
            ],

            "4G": [
                "4G AVAIL(%)",
                "4G RRC Setup Success Rate_MTN(%)"
            ],

            "5G": [
                "5G AVAIL(%)",
                "5G RRC Setup Success Rate_MTN(%)"
            ],

            "VoLTE": [
                "VoLTE AVAIL(%)",
                "VoLTE Call Setup Success Rate_MTN(%)"
            ]
        }


        technology_columns = st.columns(
            5,
            gap="small"
        )


        for index, (
            technology,
            required_columns
        ) in enumerate(
            technology_groups.items()
        ):

            detected = all(
                column
                in uploaded_df.columns

                for column
                in required_columns
            )


            with technology_columns[
                index
            ]:

                upload_kpi_card(
                    technology,

                    (
                        "✓"
                        if detected
                        else "—"
                    ),

                    (
                        "KPI group detected"
                        if detected
                        else "Not detected"
                    ),

                    (
                        "upload_kpi_technology_"
                        +
                        technology
                        .lower()
                        .replace(
                            " ",
                            "_"
                        )
                    )
                )


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.write("")


    with st.container(
        border=True,
        key="upload_panel_preview"
    ):

        panel_title(
            "Data Preview",
            "First 20 records from the uploaded KPI file"
        )


        st.dataframe(
            uploaded_df.head(
                20
            ),

            use_container_width=True,

            hide_index=True,

            height=400
        )


    # ========================================================
    # DATABASE INSERTION
    # ========================================================

    st.write("")


    with st.container(
        border=True,
        key="upload_panel_database_insert"
    ):

        panel_title(
            "Add KPI Data to Database",
            (
                "Existing Time + IHS ID combinations "
                "will automatically be skipped"
            )
        )


        if not validation[
            "valid_identifiers"
        ]:

            st.error(
                (
                    "This file cannot be added to the database "
                    "because required identification columns are missing."
                )
            )


        else:

            st.warning(
                (
                    "Only press the button after reviewing the "
                    "file summary and validation results."
                )
            )


            confirm_upload = st.checkbox(
                (
                    "I confirm that this KPI file is ready "
                    "to be added to the database"
                ),
                key="confirm_database_upload"
            )


            insert_button = st.button(
                "Add to Database",
                type="primary",
                use_container_width=True,
                disabled=not confirm_upload,
                key="insert_kpi_database"
            )


            if insert_button:

                with st.spinner(
                    "Validating and adding KPI records..."
                ):

                    result = (
                        insert_kpi_dataframe(
                            uploaded_df,
                            filename=uploaded_file.name
                        )
                    )


                # ============================================
                # INSERTION RESULT
                # ============================================

                if result[
                    "success"
                ]:

                    st.success(
                        "KPI database update completed."
                    )


                    result1, result2, result3, result4 = (
                        st.columns(
                            4,
                            gap="small"
                        )
                    )


                    with result1:

                        upload_kpi_card(
                            "Processed",
                            f"{result['total_rows']:,}",
                            "Uploaded rows",
                            "upload_result_processed"
                        )


                    with result2:

                        upload_kpi_card(
                            "Added",
                            f"{result['inserted_rows']:,}",
                            "New database records",
                            "upload_result_added"
                        )


                    with result3:

                        upload_kpi_card(
                            "Duplicates",
                            f"{result['duplicate_rows']:,}",
                            "Skipped automatically",
                            "upload_result_duplicates"
                        )


                    with result4:

                        upload_kpi_card(
                            "Rejected",
                            f"{result['rejected_rows']:,}",
                            "Invalid key/date rows",
                            "upload_result_rejected"
                        )


                    if result[
                        "inserted_rows"
                    ] > 0:

                        st.balloons()


                    st.caption(
                        (
                            f"Inserted reporting period: "
                            f"{result['earliest_date']} "
                            f"to "
                            f"{result['latest_date']}"
                        )
                    )


                    # ========================================
                    # REFRESH DATABASE SUMMARY
                    # ========================================

                    new_database_summary = (
                        get_database_summary()
                    )


                    st.write("")


                    st.markdown(
                        "#### Updated Database"
                    )


                    updated1, updated2, updated3, updated4 = (
                        st.columns(
                            4
                        )
                    )


                    with updated1:

                        st.metric(
                            "Records",
                            f"{new_database_summary['total_records']:,}"
                        )


                    with updated2:

                        st.metric(
                            "Sites",
                            f"{new_database_summary['total_sites']:,}"
                        )


                    with updated3:

                        st.metric(
                            "Reporting Days",
                            f"{new_database_summary['reporting_days']:,}"
                        )


                    with updated4:

                        st.metric(
                            "Latest KPI Date",
                            (
                                new_database_summary[
                                    "latest_date"
                                ]
                                or "—"
                            )
                        )


                else:

                    st.error(
                        result[
                            "message"
                        ]
                    )


# ============================================================
# UPLOAD HISTORY
# ============================================================

st.write("")


with st.container(
    border=True,
    key="upload_panel_history"
):

    panel_title(
        "Upload History",
        "Recent KPI database uploads"
    )


    upload_history = (
        get_upload_history(
            limit=20
        )
    )


    if upload_history.empty:

        st.info(
            "No KPI files have been added to the database yet."
        )


    else:

        st.dataframe(
            upload_history,

            use_container_width=True,

            hide_index=True,

            height=320
        )