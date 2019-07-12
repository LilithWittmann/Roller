
from dateutil.parser import parse as dateutil_parser
import json
import requests

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class VoiCrawler(Crawler):
    required_settings = []


    SERVICE_PROVIDER = "voi"
    LOCATION_BASED_CRAWLING = True

    def nearby_search(self, lat: float, lon: float, radius: int = None) -> [VehicleTrack]:
        request_url = f'https://api.voiapp.io/v1/vehicle/status/ready?lat={lat}&lng={lon}'

        result = requests.get(request_url)
        data = result.json()
        vehicle_tracks = []
        for item in data:
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["short"],
                                               provider="voi",
                                               last_seen=dateutil_parser(item["updated"]),
                                               lat=item["location"][0],
                                               lon=item["location"][1],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks
