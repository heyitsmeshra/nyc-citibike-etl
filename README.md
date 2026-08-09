# Citi Bike ETL Pipeline & Analytics Report

An end-to-end ETL pipeline that extracts live station data from the Citi Bike GBFS API, loads it into PostgreSQL, and generates a PDF analytics report on current network status and station-level bike availability.

## Overview

- **Extract** — pulls live station info/status from the Citi Bike GBFS API, with retry logic on failed requests
- **Transform** — merges station info and status into flat records, converts timestamps to US Eastern time
- **Load** — upserts data into PostgreSQL (`bike_current_status` for latest state, `bike_status_history` for time-series)
- **Report** — generates a 2-page PDF: executive summary with operational health metrics, and visual analysis of station availability

`main.py` runs the full pipeline in order: schema setup → ETL → report generation.

## Tech Stack

Python (requests, pandas, psycopg2) · PostgreSQL · Docker & Docker Compose · Matplotlib · ReportLab

## Project Structure

```
City_Bike_Pipeline/
├── analysis/
│   ├── page_1.py            # Executive summary calculations
│   ├── page_2.py            # Chart generation
│   └── generate_report.py   # PDF assembly
├── sql/                     # Schema, indexes, views
├── reports/                 # Generated PDF and charts
├── config.py
├── extract.py
├── transform.py
├── load.py
├── setup_database.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Running Locally

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bike_db
DB_USER=postgres
DB_PASSWORD=your_password
```

```bash
python main.py
```

Generates the report at `reports/Citi_Bike_Analytics_Report.pdf`.

## Running with Docker

```bash
docker-compose up --build
```

Spins up PostgreSQL and an ETL container that runs once and exits. Reports and charts are written to the host via a mounted volume. Docker Compose uses its own credentials, independent of the local `.env`.

## Database Schema

- **`bike_current_status`** — one row per station, upserted each run
- **`bike_status_history`** — append-only, keyed on `(station_id, last_reported)`, indexed for time-based queries; schema-ready for future trend analysis
- **Views** — `vw_station_status`, `vw_station_capacity`, `vw_station_demand` for operational status, capacity bucketing, and demand classification

## Report Contents

**Page 1** — Network totals, operational health breakdown, and a data-driven interpretation
**Page 2** — Top 10 stations by bike availability (%), and availability distribution across the network

Stations with zero reported capacity are excluded from percentage calculations and noted separately.

## Known Limitations

- Reflects a single point-in-time snapshot, not a time series — `bike_status_history` is schema-ready but not yet populated
- No scheduling layer; the pipeline runs on manual invocation only

## Possible Next Steps

- Schedule recurring runs against a hosted database to enable trend analysis
- Add geographic demand visualization using existing lat/long data
- Add statistical comparison of availability across capacity-size buckets