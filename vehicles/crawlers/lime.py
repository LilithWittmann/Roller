import math

from dateutil.parser import parse as dateutil_parser
import json
import requests
from shapely.geometry import Point

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class LimeCrawler(Crawler):
    required_settings = ["WEB_SESSION", "AUTHORIZATION"]

    def nearby_search(self, lat: float, lon: float, radius: int = 500) -> [VehicleTrack]:

        # i know its not exact but the best i wanted to build right now ^^

        buffer = radius / 40000000. * 360. / math.cos(lon / 360. * math.pi)
        point = Point(lat, lon).buffer(buffer)
        polygon = point.exterior.bounds

        cookies = {
            '_limebike-web_session':  self.settings.get("WEB_SESSION", None)
        }

        headers = {
            'authorization': self.settings.get('AUTHORIZATION', None)
        }

        params = (
            ('ne_lat', str(polygon[0])),
            ('ne_lng', str(polygon[1])),
            ('sw_lat', str(polygon[2])),
            ('sw_lng', str(polygon[3])),
            ('user_latitude', str(lat)),
            ('user_longitude', str(lon)),
            ('zoom', '16'),
        )

        response = requests.get('https://web-production.lime.bike/api/rider/v1/views/map', headers=headers,
                                params=params, cookies=cookies)

        vehicle_tracks = []
        for item in response.json()["data"]["attributes"]["bikes"]:
            vehicle_tracks.append(VehicleTrack(vehicle_id=f'{item["attributes"]["type_name"]}-{item["attributes"]["last_three"]}',
                                               provider="lime",
                                               last_seen=dateutil_parser(item["attributes"]["last_activity_at"]),
                                               lat=item["attributes"]["latitude"],
                                               lon=item["attributes"]["longitude"],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks