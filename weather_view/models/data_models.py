import json
from typing import List, Dict, Union, Optional

from pydantic import BaseModel


class Geolocation(BaseModel):
    latitude: float
    longitude: float
    zip: Optional[str]


class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float
    winddirection: float
    weathercode: int
    time: str


class HourlyUnits(BaseModel):
    time: str
    temperature_2m: str
    rain: str
    showers: str
    cloudcover: str


class WeatherReport(BaseModel):
    timestamp: int
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_weather: CurrentWeather
    hourly_units: HourlyUnits
    hourly: Dict[str, List[Union[str, float, int]]]

    def values(self):
        val = []
        for value in self.__dict__.values():
            if isinstance(value, BaseModel):
                value = value.json()
            elif isinstance(value, dict):
                value = json.dumps(value)
            val.append(f"'{value}'")
        return tuple(val)
