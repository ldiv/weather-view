from datetime import datetime
from functools import lru_cache
from typing import Optional

from models.app_models import WeatherReportQuery, WeatherZipQuery
from models.data_models import WeatherReport, Geolocation
from settings import WEATHER_API_URL, FORECAST_ENDPOINT, GEOCODING_API_URL
from util.http_client import SimpleHTTPClient


client = SimpleHTTPClient()


def get_weather_data_from_zip(query: WeatherZipQuery) -> Optional[WeatherReport]:
    if geo := get_geolocation(query.zip):
        query = WeatherReportQuery.default_query(geo.latitude, geo.longitude)
        return get_weather_forecast(query)


def get_weather_forecast(query: WeatherReportQuery) -> Optional[WeatherReport]:
    url = f"{WEATHER_API_URL}/{FORECAST_ENDPOINT}"
    resp = client.get(f"{url}?{query.get_raw_querystring()}")
    return WeatherReport(timestamp=datetime.now().timestamp() , **resp.json())


@lru_cache()
def get_geolocation(zip_code: str) -> Optional[Geolocation]:
    """ Queries the geocoding API to get lat/lng from zip code"""
    endpoint = "search"
    url = f"{GEOCODING_API_URL}/{endpoint}?name={zip_code}"

    resp = client.get(url)
    result = resp.json()

    if result and "results" in result:
        return Geolocation(
            latitude=result["results"][0]["latitude"],
            longitude=result["results"][0]["longitude"],
            zip=zip_code,
        )
