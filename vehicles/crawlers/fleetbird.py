from dateutil.parser import parse as dateutil_parser
import json
import requests
from datetime import datetime

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class FleetbirdCrawler(Crawler):
    required_settings = ["INSTANCE_NAME", "PROVIDER_NAME"]


    LOCATION_BASED_CRAWLING = False

    def __init__(self, settings):
        super().__init__(settings)


    def nearby_search(self, lat: float, lon: float, radius: int = None, service_area=None,
                    service_provider=None) -> [VehicleTrack]:
        request_url = f'https://{self.settings.get("INSTANCE_NAME")}.frontend.fleetbird.eu/api/prod/v1.06/map/cars/'

        result = requests.get(request_url)
        data = result.json()
        vehicle_tracks = []
        for item in data:
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["licencePlate"],
                                               provider=self.settings.get("PROVIDER_NAME"),
                                               last_seen=datetime.now(),
                                               lat=item["lat"],
                                               lon=item["lon"],
                                               raw_data=json.dumps(item)))
        return vehicle_tracks
