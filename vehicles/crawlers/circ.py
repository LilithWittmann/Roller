import math

from dateutil.parser import parse as dateutil_parser
import json
import requests
from shapely import wkt
from shapely.geometry import Point, Polygon

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class CircCrawler(Crawler):
    required_settings = []

    SERVICE_PROVIDER = "circ"
    LOCATION_BASED_CRAWLING = False

    """
    getting your tokens
    curl -X POST  -H "Content-type: application/json" -H "Accept: application/json"  "https://node.goflash.com/verification/phone/start" -d '{ "phoneCountryCode": "+49", "phoneNumber": "12345678" }'       
    curl -X POST  -H "Content-type: application/json" -H "Accept: application/json"  "https://node.goflash.com/signup/phone" -d '{ "phoneCountryCode": "+49", "phoneNumber": "12345678", "token": "345933" }'

    """

    def refresh_token(self, service_provider):

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }

        data = { "accessToken":  service_provider.settings["accessToken"],
                 "refreshToken": service_provider.settings["refreshToken"]}

        result = requests.post('https://node.goflash.com/login/refresh', headers=headers, data=json.dumps(data))

        data = result.json()

        service_provider.settings["accessToken"] = data["accessToken"]
        service_provider.settings["refreshToken"] = data["refreshToken"]
        service_provider.save()

        return service_provider



    def nearby_search(self, lat: float, lon: float, radius: int = 500, service_area=None,
                    service_provider=None) -> [VehicleTrack]:


        service_provider = self.refresh_token(service_provider)


        headers = {
            'Authorization': service_provider.settings["accessToken"],
        }
        shp = Polygon(wkt.loads(str(service_area.area).split(";")[1])).bounds

        params = (
            ('latitudeTopLeft', shp[3]),
            ('longitudeTopLeft', shp[2]),
            ('latitudeBottomRight', shp[1]),
            ('longitudeBottomRight', shp[0]),
        )


        result = requests.get('https://node.goflash.com/devices', headers=headers, params=params)
        data = result.json()
        print(data)
        vehicle_tracks = []
        for item in data["devices"]:
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["name"],
                                               provider="circ",
                                               last_seen=dateutil_parser(item["timestamp"]),
                                               lat=item["latitude"],
                                               lon=item["longitude"],
                                               battery_level=item["energyLevel"],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks