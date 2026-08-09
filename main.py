from extract import fetch_data
from transform import transform_data
from load import load_data
from setup_database import main as setup_database
from config import STATION_INFO_URL, STATION_STATUS_URL
from analysis.generate_report import generate_report


def main():

    setup_database()

    station_info = fetch_data(STATION_INFO_URL)
    station_status = fetch_data(STATION_STATUS_URL)

    if station_info is None or station_status is None:
        print("ETL Pipeline Aborted.")
        return

    transformed_data = transform_data(
        station_info,
        station_status
    )

    load_data(transformed_data)

    print("Data loaded successfully.")

    generate_report()

    print("ETL Pipeline Completed Successfully.")


if __name__ == "__main__":
    main()