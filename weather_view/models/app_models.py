from pydantic import BaseModel, validator


class SearchQuery(BaseModel):
    zip_code: str


class WeatherReportQuery(BaseModel):
    latitude: float
    longitude: float
    hourly: str
    current_weather: bool
    temperature_unit: str
    
    @classmethod
    def default_query(cls, latitude, longitude):
        return cls(
            **{
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "temperature_2m,rain,showers,cloudcover",
                "current_weather": "true",
                "temperature_unit": "fahrenheit",
            }
        )

    def get_raw_querystring(self):
        j = self.json()
        d = self.dict()
        qs = ""
        for k, v in d.items():
            qs += f"{k}={v}&"
        return qs.strip("&")


class WeatherZipQuery(BaseModel):
    zip: str

    @validator("zip")
    def is_proper_zip(cls, value: str):
        if value.isnumeric() and len(value) == 5:
            return value
        raise ValueError(f"Invalid zip format: {value}")


class WeatherCityQuery:
    city: str
