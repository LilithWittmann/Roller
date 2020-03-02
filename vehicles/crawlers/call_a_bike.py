import math

from datetime import datetime
import time
from dateutil.parser import parse as dateutil_parser
import json
import requests
from shapely import wkt
from shapely.geometry import Point, Polygon

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class CallABikeCrawler(Crawler):
    required_settings = ['ACCESS_TOKEN']

    SERVICE_PROVIDER = "call_a_bike"
    LOCATION_BASED_CRAWLING = True


    def nearby_search(self, lat: float, lon: float, radius: int = 500, service_area=None,
                    service_provider=None) -> [VehicleTrack]:


        headers = {
            'Authorization': service_provider.settings["ACCESS_TOKEN"],
        }
        shp = Polygon(wkt.loads(str(service_area.area).split(";")[1])).bounds

        params = (
            ('lat', lat),
            ('lon', lon),
            ('radius', 10000),
            ('limit', 100),
            ('providernetwork', 2),
            ('expand', 'rentalobject,area'),
        )

        result = requests.get('https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals', headers=headers, params=params)
        data = result.json()
        vehicle_tracks = []
        print(result)
        for item in data["items"]:
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["rentalObject"]["attributes"]["licenseplate"],
                                               provider=self.SERVICE_PROVIDER,
                                               last_seen=datetime.now(),
                                               lat=item["area"]["geometry"]["position"]["coordinates"][1],
                                               lon=item["area"]["geometry"]["position"]["coordinates"][0],
                                               battery_level=None,
                                               raw_data=json.dumps(item)))

        time.sleep(3)

        return vehicle_tracks