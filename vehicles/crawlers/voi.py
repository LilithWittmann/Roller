
from dateutil.parser import parse as dateutil_parser
import json
import requests
import time

from vehicles.crawlers.crawler import Crawler, VehicleTrack

class VoiCrawler(Crawler):
    required_settings = ["COUNTRY_CODE", "PHONE_NUMBER", "EMAIL", "ZONE_ID"]


    SERVICE_PROVIDER = "voi"
    LOCATION_BASED_CRAWLING = False


    def authorize(self, service_provider):
        response = request.post("https://api.voiapp.io/v1/auth/verify/phone", data=json.dumps({
            {
                "country_code": service_provider.settings["COUNTRY_CODE"],
                "phone_number": service_provider.settings["PHONE_NUMBER"]
            }
        }))
        token = response.json()["token"]

        service_provider.settings["loginToken"] = token
        service_provider.save()

        return service_provider


    def sms_hook(self, service_provider, sms):
        import re

        if not "VOI" in sms:
            return False

        m = re.search(r'[0-9]{6}', sms)

        response = request.post("https://api.voiapp.io/v1/auth/verify/phone", data=json.dumps({
            {
                "code": m.group(0),
                "token": service_provider.settings["loginToken"]
            }
        }))


        response = request.post("https://api.voiapp.io/v1/auth/verify/presence", data=json.dumps({
            {
                "email": service_provider.settings["EMAIL"],
                "token": service_provider.settings["loginToken"]
            }
        }))
        service_provider.settings["authenticationToken"] = response.json()["authenticationToken"]
        service_provider.save()


    def refresh_token(self, service_provider):

        response = request.post("https://api.voiapp.io/v1/auth/session", data=json.dumps({
            {
                "authenticationToken": service_provider.settings["authenticationToken"]
            }
        }))

        tokens = response.json()

        service_provider.settings["authenticationToken"] = tokens["authenticationToken"]
        service_provider.settings["accessToken"] = tokens["accessToken"]
        service_provider.save()

        return service_provider



    def nearby_search(self, lat: float, lon: float, radius: int = None, service_area=None,
                    service_provider=None) -> [VehicleTrack]:


        service_provider = self.refresh_token(service_provider)
        headers = {
            'x-access-token': service_provider.settings["accessToken"],
        }
        request_url = f'https://api.voiapp.io/v2/rides/vehicles?zone_id={self.settings.get("ZONE_ID")}'

        result = requests.get(request_url,headers=headers)
        data = result.json()
        vehicle_tracks = []
        for item in data:
            vehicle_tracks.append(VehicleTrack(vehicle_id=item["short"],
                                               provider="voi",
                                               last_seen=dateutil_parser(item["updated"]),
                                               lat=item["location"][0],
                                               lon=item["location"][1],
                                               battery_level=item["battery"],
                                               raw_data=json.dumps(item)))

        return vehicle_tracks
