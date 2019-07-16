import importlib
import json
import math
from datetime import timedelta
from os.path import join, exists

from django.apps import apps
from django.core.management.base import BaseCommand
import argparse
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon

from vehicles.models import ServiceTrackingArea, SubUrb, TripEstimation, TripTypes


class Command(BaseCommand):
    help = 'classify our estimated trips'

    def handle(self, *args, **options):
        for trip in TripEstimation.objects.all():
            if not trip.route_duration_estimation:
                continue

            if (trip.duration < timedelta(seconds=25 * 60) and trip.duration < trip.route_duration_estimation * 2.5) \
                    or (trip.duration < timedelta(seconds=12 * 60) and trip.battery_consumption > 2 \
                        and trip.route_distance_estimation > 300):
                print("probably nearby trip")
                trip.trip_type = TripTypes.SHORT_TRIP
            elif trip.duration > timedelta(seconds=25 * 60) and trip.duration < trip.route_duration_estimation * 2.5 \
                    and trip.route_distance_estimation > 3000:
                print("probably long distance trip")
                trip.trip_type = TripTypes.LONG_TRIP
            elif trip.duration > timedelta(seconds=10 * 60) \
                    and trip.battery_consumption * 4 > trip.duration.seconds / 60:
                print("are you a tourist?!")
                trip.trip_type = TripTypes.FUN_TRIP
            elif trip.battery_consumption  < -5:
                trip.trip_type = TripTypes.DEPLOYMENT
                print("recently deployed?!")
            else:
                print("something something")
                trip.trip_type = TripTypes.UNKNOWN
                print(trip.route_distance_estimation)
                print(trip.duration)
                print(trip.vehicle_id)
                print(trip.battery_consumption)
                print(trip.start_point.battery_level)
                print(trip.end_point.battery_level)


            trip.save()
