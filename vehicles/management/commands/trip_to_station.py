import importlib
import json
import math
from os.path import join, exists

import overpy
from django.apps import apps
from django.core.management.base import BaseCommand
import argparse
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
from shapely import wkt
from shapely.geometry import Polygon

from vehicles.models import ServiceTrackingArea, SubUrb, PublicTransportStation, VehicleLocationTrack, TripEstimation
from vehicles.services import PublicTransportService


class Command(BaseCommand):

    help = 'assigns all vehiclelocationtracks to public transport stations if there are any'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        for trip in TripEstimation.objects.all():
            PublicTransportService.assign_station_to_trip_estimation(trip)