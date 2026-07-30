import requests
import time

from config import STATION_INFO_URL, STATION_STATUS_URL, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY


def fetch_data(url):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            data = response.json()

            return data["data"]["stations"]

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds")
                time.sleep(RETRY_DELAY)
            else:
                print("Maximum retry attempts reached.")
                return None


if __name__ == "__main__":
    station_info = fetch_data(STATION_INFO_URL)
    station_status = fetch_data(STATION_STATUS_URL)

    if station_info is not None:
        print(f"Station Information Records: {len(station_info)}")

    if station_status is not None:
        print(f"Station Status Records: {len(station_status)}")