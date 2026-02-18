"""
Exercise 4.C.5 — Building an API Client Class
Guide: docs/python-guide/04-data-and-apis.md

Tasks:
1. Create a WeatherData dataclass for structured responses
2. Create a custom WeatherAPIError exception
3. Build a WeatherClient class with requests.Session
4. Make it a context manager (__enter__/__exit__)
5. Handle all error cases
"""

import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    """Structured weather data."""
    city: str
    temperature_c: float
    description: str
    humidity: int
    wind_speed: float

    @property
    def temperature_f(self) -> float:
        # TODO: Implement
        pass


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass


class WeatherClient:
    """Weather API client with session management."""

    BASE_URL = "https://wttr.in"

    def __init__(self, timeout: int = 10):
        # TODO: Initialize session
        pass

    def get_weather(self, city: str) -> Optional[WeatherData]:
        """Get current weather for a city."""
        # TODO: Implement
        pass

    def close(self):
        """Close the HTTP session."""
        # TODO: Implement
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# TODO: Test with context manager
# with WeatherClient() as client:
#     for city in ["London", "Tokyo", "New York"]:
#         weather = client.get_weather(city)
#         print(weather)
