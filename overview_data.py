import numpy as np
import pandas as pd


# ============================================================
# RANDOM GENERATOR
# ============================================================

RNG = np.random.default_rng(2026)


# ============================================================
# HELPER
# ============================================================

def bounded_walk(
    start,
    low,
    high,
    n=30,
    volatility=0.18
):

    values = [start]

    for _ in range(n - 1):

        next_value = (
            values[-1]
            + RNG.normal(0, volatility)
        )

        values.append(
            np.clip(
                next_value,
                low,
                high
            )
        )

    return np.round(values, 3)


# ============================================================
# DAILY NETWORK KPI DATA
# ============================================================

def generate_daily_kpis(days=30):

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=days,
        freq="D"
    )

    availability = bounded_walk(
        98.45,
        96.5,
        99.95,
        days,
        0.15
    )

    cssr = bounded_walk(
        98.12,
        96.5,
        99.8,
        days,
        0.18
    )

    dcr = bounded_walk(
        1.23,
        0.30,
        2.50,
        days,
        0.08
    )

    hosr = bounded_walk(
        97.82,
        94.5,
        99.8,
        days,
        0.20
    )

    rrc = bounded_walk(
        99.35,
        97.0,
        99.95,
        days,
        0.12
    )

    return pd.DataFrame({

        "Date": dates,

        "Availability": availability,

        "CSSR": cssr,

        "DCR": dcr,

        "HOSR": hosr,

        "RRC": rrc,

        "Traffic_2G": np.round(
            RNG.uniform(0.8, 1.5, days),
            2
        ),

        "Traffic_3G": np.round(
            RNG.uniform(2.2, 3.8, days),
            2
        ),

        "Traffic_4G": np.round(
            RNG.uniform(6.0, 9.0, days),
            2
        ),

        "Traffic_5G": np.round(
            RNG.uniform(0.7, 1.8, days),
            2
        ),

        "Latency": np.round(
            RNG.uniform(25, 40, days),
            1
        ),

        "Active_Users": np.round(
            RNG.uniform(3.8, 4.8, days),
            2
        ),

        "Voice_Attempts": np.round(
            RNG.uniform(20, 26, days),
            2
        )

    })


# ============================================================
# TECHNOLOGY AVAILABILITY
# ============================================================

def generate_technology_availability():

    return pd.DataFrame({

        "Technology": [
            "2G",
            "3G",
            "4G",
            "5G",
            "VoLTE"
        ],

        "Availability": [
            97.21,
            97.89,
            99.12,
            99.24,
            99.05
        ]

    })


# ============================================================
# WORST CELLS
# ============================================================

def generate_worst_cells(n=5):

    technologies = [
        "2G",
        "3G",
        "4G",
        "5G"
    ]

    rows = []

    for i in range(n):

        technology = RNG.choice(
            technologies
        )

        prefix = {

            "2G": "BSC",

            "3G": "RNC",

            "4G": "LTE",

            "5G": "NR"

        }[technology]

        rows.append({

            "Rank":
                i + 1,

            "Cell Name":
                f"{prefix}_{RNG.integers(10,999):03d}_CELL_{RNG.integers(1000,9999)}",

            "Technology":
                technology,

            "DCR (%)":
                round(
                    float(
                        RNG.uniform(
                            2.1,
                            6.2
                        )
                    ),
                    2
                ),

            "Availability (%)":
                round(
                    float(
                        RNG.uniform(
                            94.5,
                            98.7
                        )
                    ),
                    2
                ),

            "Traffic (GB)":
                round(
                    float(
                        RNG.uniform(
                            300,
                            950
                        )
                    ),
                    1
                )

        })

    df = pd.DataFrame(rows)

    return df.sort_values(
        "DCR (%)",
        ascending=False
    ).reset_index(drop=True)


# ============================================================
# ALARMS
# ============================================================

def generate_alarms(n=12):

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

    alarm_names = [

        "Cell Down",

        "Transmission Down",

        "High PRB Utilization",

        "Abnormal Call Drop Rate",

        "High Latency",

        "Low RRC Success Rate",

        "High Packet Loss",

        "High TCH Congestion",

        "Low HOSR"

    ]

    rows = []

    for i in range(n):

        rows.append({

            "Time":
                (
                    pd.Timestamp.now()
                    - pd.Timedelta(
                        minutes=int(
                            i * 13
                        )
                    )
                ).strftime(
                    "%d %b %Y %H:%M"
                ),

            "Severity":
                RNG.choice(
                    severity_options,
                    p=[
                        0.15,
                        0.30,
                        0.35,
                        0.20
                    ]
                ),

            "Alarm":
                RNG.choice(
                    alarm_names
                ),

            "Technology":
                RNG.choice(
                    technology_options
                ),

            "Site":
                f"SITE_{RNG.integers(1,999):03d}",

            "Status":
                RNG.choice(
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
# CELL STATUS DISTRIBUTION
# ============================================================

def generate_cell_distribution():

    return pd.DataFrame({

        "Status": [
            "Excellent",
            "Good",
            "Average",
            "Poor"
        ],

        "Count": [
            68.5,
            21.7,
            7.6,
            2.2
        ]

    })


# ============================================================
# TRAFFIC DISTRIBUTION
# ============================================================

def generate_traffic_distribution():

    return pd.DataFrame({

        "Technology": [
            "2G",
            "3G",
            "4G",
            "5G"
        ],

        "Traffic": [
            1.25,
            3.45,
            7.95,
            0.92
        ]

    })