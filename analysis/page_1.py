import pandas as pd
import psycopg2

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def load_current_status():
    """
    Load the latest station snapshot from the database.
    """

    query = """
    SELECT
        station_id,
        name,
        capacity,
        num_bikes_available,
        num_docks_available,
        is_installed,
        is_renting,
        is_returning
    FROM bike_current_status;
    """

    with get_connection() as connection:

        current_df = pd.read_sql(
            query,
            connection
        )

    return current_df


def calculate_summary(current_df):
    """
    Calculate overall network statistics.
    """

    total_stations = len(current_df)

    total_capacity = current_df["capacity"].sum()

    total_bikes = current_df["num_bikes_available"].sum()

    total_docks = current_df["num_docks_available"].sum()

    average_capacity = current_df["capacity"].mean()

    bike_availability_ratio = (
        (total_bikes / total_capacity) * 100
        if total_capacity > 0 else 0
    )

    dock_availability_ratio = (
        (total_docks / total_capacity) * 100
        if total_capacity > 0 else 0
    )

    return {

        "total_stations": total_stations,

        "total_capacity": int(total_capacity),

        "total_bikes": int(total_bikes),

        "total_docks": int(total_docks),

        "average_capacity": round(
            average_capacity,
            1
        ),

        "bike_availability_ratio": round(
            bike_availability_ratio,
            2
        ),

        "dock_availability_ratio": round(
            dock_availability_ratio,
            2
        )

    }


def calculate_operational_health(current_df):
    """
    Calculate station operational status.
    """

    operational = len(

        current_df[

            (current_df["is_installed"] == 1) &
            (current_df["is_renting"] == 1) &
            (current_df["is_returning"] == 1)

        ]

    )

    partially_available = len(

        current_df[

            (current_df["is_installed"] == 1) &
            (
                (current_df["is_renting"] == 0) |
                (current_df["is_returning"] == 0)
            )

        ]

    )

    out_of_service = len(

        current_df[
            current_df["is_installed"] == 0
        ]

    )

    total = len(current_df)

    return {

        "operational": operational,

        "partially_available": partially_available,

        "out_of_service": out_of_service,

        "operational_percent": round(
            (operational / total) * 100,
            2
        ),

        "partial_percent": round(
            (partially_available / total) * 100,
            2
        ),

        "out_percent": round(
            (out_of_service / total) * 100,
            2
        )

    }


def generate_interpretation(summary, health):
    """
    Generate a short interpretation for the executive summary.
    """

    interpretation = []

    if health["operational_percent"] >= 95:

        interpretation.append(
            "The network is operating normally, with almost all stations fully operational."
        )

    elif health["operational_percent"] >= 85:

        interpretation.append(
            "Most stations are operational, with only a small proportion experiencing limited service."
        )

    else:

        interpretation.append(
            "Operational availability is lower than expected, indicating noticeable service disruptions."
        )

    interpretation.append(

        f"Currently, {summary['bike_availability_ratio']}% "
        f"of the network capacity is occupied by available bikes, "
        f"while {summary['dock_availability_ratio']}% "
        f"remains available for docking."

    )

    return " ".join(interpretation)


def get_page1_data():
    """
    Prepare all data required for Page 1 of the PDF report.
    """

    current_df = load_current_status()

    summary = calculate_summary(
        current_df
    )

    health = calculate_operational_health(
        current_df
    )

    interpretation = generate_interpretation(
        summary,
        health
    )

    return {

        "current_df": current_df,

        "summary": summary,

        "health": health,

        "interpretation": interpretation

    }