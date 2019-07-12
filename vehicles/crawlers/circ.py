import math

from dateutil.parser import parse as dateutil_parser
import json
import requests
from shapely.geometry import Point

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class CircCrawler(Crawler):
    required_settings = []

    SERVICE_PROVIDER = "circ"
    LOCATION_BASED_CRAWLING = True

    def nearby_search(self, lat: float, lon: float, radius: int = 500) -> [VehicleTrack]:

        # i know its not exact but the best i wanted to build right now ^^

        buffer = radius / 40000000. * 360. / math.cos(lon / 360. * math.pi)
        delta = (int(buffer * 1000) + 1) / 1000.0
        request_url = f'https://api.goflash.com/api/Mobile/Scooters?userLatitude={lat}&userLongitude={lon}' \
            f'&lang=en&latitude={lat}&longitude={lon}&latitudeDelta={delta}&longitudeDelta={delta}'
        print(request_url)
        result = requests.get(request_url)
        data = result.json()
        vehicle_tracks = []
        for item in data["Data"]["Scooters"]:
            print(item)
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["licencePlate"],
                                               provider="tier",
                                               last_seen=dateutil_parser(item["lastStateChange"]),
                                               lat=item["lat"],
                                               lon=item["lng"],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks