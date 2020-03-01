import importlib
import math
from os.path import join, exists

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from shapely.geometry import Point, Polygon
from shapely import wkt
from shapely.geometry import shape, Point
import geojson
import json
from datetime import date, timedelta
import time

from vehicles.models import ServiceTrackingArea, Vehicle, VehicleLocationTrack, TripEstimation
from vehicles.services import PriceEstimationService, RouteEstimationService, PublicTransportService
from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'searches for routes in the dataset for today'

    def handle(self, *args, **options):

        for vehicle in Vehicle.objects.all():
            last_track = None
            for track in vehicle.location_track \
                    .filter(last_seen__gte=date.today() - timedelta(hours=2)).order_by('-last_seen'):
                print(track.updated_at)
                if TripEstimation.objects.filter(start_point=track).exists():
                    break
                if last_track:
                    radius = 180
                    buffer = (radius / 40000000. * 360. / math.cos(track.position.x / 360. * math.pi))
                    trip_duration = int((last_track.last_seen - track.last_seen).total_seconds() / 60)
                    if not Point(track.position.x, track.position.y) \
                            .within(Point(last_track.position.x, last_track.position.y).buffer(buffer)) \
                            and (track.battery_level - last_track.battery_level) > 2 and trip_duration < 180:

                        print(track.vehicle)
                        print("battery consumtion: " + str(track.battery_level - last_track.battery_level))
                        print("trip duration: " + str(trip_duration))
                        print(str(track.position) + " vs " + str(last_track.position))

                        if not TripEstimation.objects.filter(start_point=last_track).exists() and not \
                                TripEstimation.objects.filter(end_point=track).exists():
                            print("new trip!")
                            price_estimation = PriceEstimationService.calculate_price(track, last_track)
                            route_estimation = RouteEstimationService.get_routing(
                                [track.position.x, track.position.y],
                                [last_track.position.x, last_track.position.y],
                            )
                            estimated_time = timedelta(seconds=route_estimation["paths"][0]["time"] / 1000),
                            estimated_distance = int(route_estimation["paths"][0]["distance"])
                            print(estimated_distance)

                            trp = TripEstimation.objects.create(vehicle=vehicle, start_point=track,
                                                                end_point=last_track,
                                                                duration=(last_track.last_seen - track.last_seen),
                                                                price_estimation=price_estimation,
                                                                route_estimation=GEOSGeometry(
                                                                    json.dumps(route_estimation["paths"][0]["points"]),
                                                                ),
                                                                route_duration_estimation=estimated_time,
                                                                route_distance_estimation=estimated_distance)
                            PublicTransportService.assign_station_to_trip_estimation(trp)

                if track:
                    last_track = track
