import psycopg2

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def load_data(transformed_data):

    connection=None
    cursor=None

    try:

        connection=psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor=connection.cursor()

        current_status_query="""
        INSERT INTO bike_current_status(
            station_id,
            name,
            short_name,
            latitude,
            longitude,
            capacity,
            num_bikes_available,
            num_docks_available,
            is_installed,
            is_renting,
            is_returning,
            last_reported
        )
        VALUES(
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        ON CONFLICT(station_id)
        DO UPDATE SET
            capacity=EXCLUDED.capacity,
            num_bikes_available=EXCLUDED.num_bikes_available,
            num_docks_available=EXCLUDED.num_docks_available,
            is_installed=EXCLUDED.is_installed,
            is_renting=EXCLUDED.is_renting,
            is_returning=EXCLUDED.is_returning,
            last_reported=EXCLUDED.last_reported;
        """

        history_query="""
        INSERT INTO bike_status_history(
            station_id,
            name,
            short_name,
            latitude,
            longitude,
            capacity,
            num_bikes_available,
            num_docks_available,
            is_installed,
            is_renting,
            is_returning,
            last_reported
        )
        VALUES(
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        ON CONFLICT(station_id,last_reported)
        DO NOTHING;
        """

        for station in transformed_data:

            values=(
                station["station_id"],
                station["name"],
                station["short_name"],
                station["latitude"],
                station["longitude"],
                station["capacity"],
                station["num_bikes_available"],
                station["num_docks_available"],
                station["is_installed"],
                station["is_renting"],
                station["is_returning"],
                station["last_reported"]
            )

            cursor.execute(current_status_query,values)
            cursor.execute(history_query,values)

        connection.commit()

        print("Data loaded successfully.")

    except psycopg2.Error as e:
        print(f"Database Error: {e}")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()