from dateutil.parser import parse as dateutil_parser
import json
import requests

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class TierCrawler(Crawler):
    required_settings = ["API_KEY"]

    def nearby_search(self, lat: float, lon: float, radius: int = 500) -> [VehicleTrack]:
        request_url = f'https://platform.tier-services.io/vehicle?lat={lat}&lng={lon}&radius={radius}'
        headers = {'X-Api-Key': self.settings.get("API_KEY")}
        result = requests.get(request_url, headers=headers)
        data = result.json()
        vehicle_tracks = []
        for item in data["data"]:
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["licencePlate"],
                                               provider="tier",
                                               last_seen=dateutil_parser(item["lastStateChange"]),
                                               lat=item["lat"],
                                               lon=item["lng"],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks
