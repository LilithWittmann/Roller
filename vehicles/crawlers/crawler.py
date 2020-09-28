import datetime
from abc import abstractmethod, ABC

import requests
from django.contrib.gis.geos import Point


class VehicleTrack(object):

    SERVICE_PROVIDER = None
    LOCATION_BASED_CRAWLING = True

    def __init__(self, vehicle_id: str, lat: int, lon: int, raw_data: str, provider: str, last_seen: datetime = None,
                 battery_level: int = None, vehicle_type = "escooter"):
        self.id = vehicle_id
        self.lat = lat
        self.lon = lon
        self.provider = provider
        self.raw_data = raw_data
        self.last_seen = last_seen
        self.battery_level = battery_level
        self.vehicle_type = vehicle_type

    @property
    def location(self):
        return Point(round(self.lon, 5), round(self.lat, 5))

    @property
    def vehicle_id(self) -> str:
        return f'{self.provider}-{self.id}'

    def __str__(self):
        return self.vehicle_id


class Crawler(ABC):
    required_settings = []

    def __init__(self, settings):

        for setting in self.required_settings:
            if setting not in settings:
                raise Exception(f'{setting} has to be configured')

        self.settings = settings

    @abstractmethod
    def nearby_search(self, lat: float, lon: float, radius: int = 500) -> [VehicleTrack]:
        pass

    def authorize(self, service_provider):
        pass
