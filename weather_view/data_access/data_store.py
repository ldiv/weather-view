import json
from typing import Optional, List

from models.data_models import Geolocation, WeatherReport
from data_access.db import AbstractDatabase, Filter


class DataStore:
    _geolocation_key = "geolocation"
    _forecast_key = "weatherreport"

    def __init__(self, database: AbstractDatabase):
        self.db = database

    @staticmethod
    def _get_top(entries: List):
        if entries:
            return entries[0]

    def get_geolocation(self, zip) -> Optional[Geolocation]:
        filter_ = Filter(**{"condition": {"zip": zip}})
        result = self.db.get_entries(self._geolocation_key, filter_)
        if result:
            result = result[0]
            return Geolocation(latitude=result["latitude"], longitude=result["longitude"])

    def store_geolocation(self, geolocation: Geolocation) -> int:
        id_ = self.db.insert_entry(self._geolocation_key, geolocation.dict())
        return id_

    def get_report(self, geolocation: Geolocation) -> Optional[WeatherReport]:
        filter_ = Filter(**{
            "condition": {
                "latitude": geolocation.latitude,"longitude": geolocation.longitude
            },
            "sort": "timestamp DESC"
        })
        result = self._get_top(self.db.get_entries(self._forecast_key, filter_))

        if result:
            # TODO: move this logic to the model
            result["current_weather"] = json.loads(result["current_weather"])
            result["hourly_units"] = json.loads(result["hourly_units"])
            result["hourly"] = json.loads(result["hourly"])

            return WeatherReport(**dict(result))

    def store_report(self, report: WeatherReport) -> int:
        values = report.dict()
        # TODO: move this logic to the model
        values["current_weather"] = json.dumps(values["current_weather"])
        values["hourly_units"] = json.dumps(values["hourly_units"])
        values["hourly"] = json.dumps(values["hourly"])
        id_ = self.db.insert_entry(self._forecast_key, values)
        return id_
