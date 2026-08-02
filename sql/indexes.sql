-- Station index
CREATE INDEX IF NOT EXISTS idx_station
ON bike_status_history(station_id);

-- Timestamp index
CREATE INDEX IF NOT EXISTS idx_time
ON bike_status_history(last_reported);

-- Station + Timestamp index
CREATE INDEX IF NOT EXISTS idx_station_time
ON bike_status_history(station_id, last_reported);