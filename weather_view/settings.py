from pathlib import Path

from database.sqlite import SQLite, SQLiteConnection


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = str(Path(BASE_DIR, "static"))
TEMPLATES_DIR = str(Path(BASE_DIR, "templates"))

WEATHER_API_URL = "https://api.open-meteo.com/v1"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1"
FORECAST_ENDPOINT = "forecast"

APP_PORT = 8813

DB_PATH = BASE_DIR
DB_NAME = "weather-view.sqlite"

database_class = SQLite
database_conn_info = SQLiteConnection(database_path=f"{DB_PATH}/{DB_NAME}")
