from time import time
from typing import Optional

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from data_access.data_store import DataStore
from models.app_models import WeatherReportQuery, WeatherZipQuery
from models.data_models import WeatherReport, Geolocation
from settings import STATIC_DIR, TEMPLATES_DIR, database_class, database_conn_info
from weather_api import get_weather_forecast, get_geolocation
from util.log import logger


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

database = database_class(database_conn_info, models=[WeatherReport, Geolocation])
datastore = DataStore(database)


@app.get("/")
async def main_page(request: Request) -> Response:
    return templates.TemplateResponse("weather_view.html", {"request": request})


@app.post("/report")
async def report(request: Request, query: WeatherZipQuery) -> JSONResponse:
    geolocation = datastore.get_geolocation(query.zip)
    if not geolocation:
        geolocation = _get_geolocation_from_api(query.zip)
    # If a recent report exits return that
    weather_forecast = datastore.get_report(geolocation)
    if not weather_forecast or not _is_recent(weather_forecast.timestamp):
        weather_forecast = _get_weather_report_from_api(geolocation)
        if not weather_forecast:
            raise HTTPException(status_code=500, detail="Something went wrong")

    return JSONResponse(weather_forecast.json())


def _is_recent(timestamp, time_limit=3600):
    return int(time()) - timestamp < time_limit


def _get_weather_report_from_api(geolocation: Geolocation) -> Optional[WeatherReport]:
    query = WeatherReportQuery.default_query(geolocation.latitude, geolocation.longitude)
    weather_forecast = get_weather_forecast(query)
    if not weather_forecast:
        return None
    row_id = datastore.store_report(weather_forecast)
    if not row_id:
        logger.warning("API response not saved to database")
    return weather_forecast


def _get_geolocation_from_api(zip_code: str) -> Geolocation:
    geolocation = get_geolocation(zip_code)
    row_id = datastore.store_geolocation(geolocation)
    if not row_id:
        logger.warning("API response not saved to database")
    return geolocation
