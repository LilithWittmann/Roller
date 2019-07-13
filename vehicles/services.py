import requests
from django.conf import settings
from serious_django_services import Service
from vehicles.models import ServiceTrackingArea, Pricing, VehicleLocationTrack


class PriceEstimationService(Service):

    service_exceptions = ()

    @classmethod
    def calculate_price(cls, start: VehicleLocationTrack, end: VehicleLocationTrack) -> float:
        area = ServiceTrackingArea.objects.filter(area__contains=start.position).first()
        try:
            pricing = Pricing.objects.get(service_provider=start.vehicle.service_provider, service_area=area)
        except Pricing.DoesNotExist:
            return None

        return pricing.unlock_fee + int((end.last_seen - start.last_seen).total_seconds()/60) * pricing.minute_price


class RouteEstimationService(Service):
    service_exceptions = ()

    @classmethod
    def get_routing(cls, start_point: [float, float], end_point: [float, float]):
        """get informations like distance, time and geojson for the calculated route"""
        # no I'm not drunk but the people behind the graphhopper api might have been when they built it
        routing_coords = [",".join([str(itm) for itm in reversed(start_point)])]

        routing_coords.append(
            ",".join([str(itm) for itm in reversed(end_point)]))

        routing_request = {
            "key": settings.GRAPH_HOPPER_APIKEY,
            "vehicle": "bike",
            "point": routing_coords,
            "locale": "de",
            "details": "time",
            "points_encoded": False,
            "instructions": False
        }
        response = requests.get("https://graphhopper.com/api/1/route", params=routing_request)
        return response.json()
