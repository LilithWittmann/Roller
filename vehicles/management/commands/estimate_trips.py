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
from datetime import date

from vehicles.models import ServiceTrackingArea, Vehicle, VehicleLocationTrack, TripEstimation
from vehicles.services import PriceEstimationService, RouteEstimationService
from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):

    help = 'searches for routes in the dataset for today'

    def handle(self, *args, **options):

        for vehicle in Vehicle.objects.all():
            last_track = None
            for track in vehicle.location_track.filter(updated_at_day=date.today()).order_by('updated_at'):
                if last_track:
                    radius = 150
                    buffer = (radius / 40000000. * 360. / math.cos(track.position.x / 360. * math.pi))
                    trip_duration = int((track.last_seen - last_track.last_seen).total_seconds()/60)
                    if not Point(track.position.x, track.position.y)\
                            .within(Point(last_track.position.x, last_track.position.y).buffer(buffer))\
                            and (last_track.battery_level - track.battery_level) > 1 and trip_duration < 300:

                        print(track.vehicle)
                        print("battery consumtion: "+ str(last_track.battery_level - track.battery_level))
                        print("trip duration: "+ str(trip_duration))
                        print(str(track.position)+" vs "+str(last_track.position))

                        if not TripEstimation.objects.filter(start_point=last_track, end_point=track).exists():
                            print("new trip!")
                            price_estimation = PriceEstimationService.calculate_price(last_track, track)
                            route_estimation = RouteEstimationService.get_routing(
                                [last_track.position.x, last_track.position.y],
                                [track.position.x, track.position.y],
                            )

                            TripEstimation.objects.create(vehicle=vehicle, start_point=last_track, end_point=track,
                                                          duration=(track.last_seen - last_track.last_seen),
                                                          price_estimation=price_estimation,
                                                          route_estimation=GEOSGeometry(json.dumps(route_estimation["paths"][0]["points"])))


                last_track = track