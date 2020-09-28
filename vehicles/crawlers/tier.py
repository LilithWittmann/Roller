from dateutil.parser import parse as dateutil_parser
import json
import requests

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class TierCrawler(Crawler):
    required_settings = ["API_KEY", "ZONE_ID"]


    SERVICE_PROVIDER = "tier"
    LOCATION_BASED_CRAWLING = False

    def nearby_search(self, lat: float, lon: float, radius: int = 500, service_area=None,
                    service_provider=None) -> [VehicleTrack]:
        request_url = f'https://platform.tier-services.io/v2/vehicle?zoneId={self.settings.get("ZONE_ID")}'
        headers = {'X-Api-Key': self.settings.get("API_KEY")}
        result = requests.get(request_url, headers=headers,timeout=5)
        data = result.json()
        vehicle_tracks = []
        v_mapping = {
            "emoped": "emoped",
            "escooter": "escooter"
        }
        print(data["data"])
        for item in data["data"]:
            item = item["attributes"]
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["licencePlate"],
                                               provider="tier",
                                               last_seen=dateutil_parser(item["lastLocationUpdate"]),
                                               lat=item["lat"],
                                               lon=item["lng"],
                                               battery_level=item["batteryLevel"],
                                               vehicle_type=v_mapping[item["vehicleType"]],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks
