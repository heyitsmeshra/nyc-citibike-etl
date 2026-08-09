from datetime import datetime, UTC
from zoneinfo import ZoneInfo



def transform_data(station_info, station_status):

    status_lookup={}

    for status in station_status:
        status_lookup[status["station_id"]]=status

    transformed_data=[]

    for info in station_info:

        station_id=info["station_id"]

        if station_id in status_lookup:

            merged_station={
                "station_id":info["station_id"],
                "name":info["name"],
                "short_name":info["short_name"],
                "latitude":info["lat"],
                "longitude":info["lon"],
                "capacity":info["capacity"],
                "num_bikes_available":status_lookup[station_id]["num_bikes_available"],
                "num_docks_available":status_lookup[station_id]["num_docks_available"],
                "is_installed":status_lookup[station_id]["is_installed"],
                "is_renting":status_lookup[station_id]["is_renting"],
                "is_returning":status_lookup[station_id]["is_returning"],
                "last_reported":datetime.fromtimestamp(
                    status_lookup[station_id]["last_reported"],
                    tz=UTC
                ).astimezone(
                    ZoneInfo("America/New_York")
                ).replace(tzinfo=None)
            }

            transformed_data.append(merged_station)

    return transformed_data