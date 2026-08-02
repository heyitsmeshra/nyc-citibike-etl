CREATE OR REPLACE VIEW vw_station_status AS
SELECT
    station_id,
    name,
    capacity,
    num_bikes_available,
    num_docks_available,
    is_installed,
    is_renting,
    is_returning,
    CASE
        WHEN is_installed=0 THEN 'Not Installed'
        WHEN is_renting=0 AND is_returning=0 THEN 'Out of Service'
        WHEN is_renting=0 THEN 'Renting Disabled'
        WHEN is_returning=0 THEN 'Returning Disabled'
        ELSE 'Operational'
    END AS operational_status,
    last_reported
FROM bike_current_status;


CREATE OR REPLACE VIEW vw_station_capacity AS
SELECT
    station_id,
    name,
    capacity,
    num_bikes_available,
    num_docks_available,
    CASE
        WHEN capacity<15 THEN 'Small'
        WHEN capacity<=35 THEN 'Medium'
        ELSE 'Large'
    END AS capacity_size,
    last_reported
FROM bike_current_status;


CREATE OR REPLACE VIEW vw_station_demand AS
SELECT
    station_id,
    name,
    capacity,
    num_bikes_available,
    num_docks_available,
    ROUND((num_bikes_available::NUMERIC/capacity)*100,2) AS bike_percent,
    CASE
        WHEN is_installed=0 THEN 'Not Installed'
        WHEN is_renting=0 AND is_returning=0 THEN 'Out of Service'
        WHEN num_bikes_available=0 THEN 'Needs Refill'
        WHEN num_docks_available=0 THEN 'Needs Pickup'
        WHEN (num_bikes_available::NUMERIC/capacity)*100 <= 20 THEN 'Low Bikes'
        WHEN (num_bikes_available::NUMERIC/capacity)*100 >= 80 THEN 'Nearly Full'
        ELSE 'Balanced'
    END AS demand_status,
    last_reported
FROM bike_current_status
WHERE capacity>0;