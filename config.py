import os
from dotenv import load_dotenv

load_dotenv()

# API URLs
STATION_INFO_URL="https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
STATION_STATUS_URL="https://gbfs.citibikenyc.com/gbfs/en/station_status.json"

# API Configuration
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=2

# Database Configuration
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")