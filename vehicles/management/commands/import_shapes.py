import importlib
import json
import math
from os.path import join, exists

from django.apps import apps
from django.core.management.base import BaseCommand
import argparse
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon

from vehicles.models import ServiceTrackingArea, SubUrb


class Command(BaseCommand):

    help = 'searches for routes in the dataset for today'

    def add_arguments(self, parser):
        parser.add_argument('shapefile', type=str)
        parser.add_argument('service_area', type=int)

    def handle(self, *args, **options):
        print(options["shapefile"])
        service_area = ServiceTrackingArea.objects.get(id=options["service_area"])
        with open(options["shapefile"]) as json_file:
            data = json.load(json_file)
            print(data)
            print(service_area)

            for feat in data["features"]:
                print(feat["properties"]["OTEIL"])
                try:
                    geom = GEOSGeometry(json.dumps(feat["geometry"]))
                    if type(geom) != MultiPolygon:
                        geom = MultiPolygon(geom)
                    SubUrb.objects.create(area=geom,
                                          service_area=service_area, name=feat["properties"]["OTEIL"])
                except Exception as e:
                    print(e)