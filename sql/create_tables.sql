CREATE TABLE bike_current_status (
    station_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    short_name TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    capacity INTEGER NOT NULL,
    num_bikes_available INTEGER NOT NULL,
    num_docks_available INTEGER NOT NULL,
    is_installed SMALLINT NOT NULL,
    is_renting SMALLINT NOT NULL,
    is_returning SMALLINT NOT NULL,
    last_reported TIMESTAMP NOT NULL
);

CREATE TABLE bike_status_history (
    station_id TEXT NOT NULL,
    name TEXT NOT NULL,
    short_name TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    capacity INTEGER NOT NULL,
    num_bikes_available INTEGER NOT NULL,
    num_docks_available INTEGER NOT NULL,
    is_installed SMALLINT NOT NULL,
    is_renting SMALLINT NOT NULL,
    is_returning SMALLINT NOT NULL,
    last_reported TIMESTAMP NOT NULL,

    PRIMARY KEY (station_id, last_reported)
);