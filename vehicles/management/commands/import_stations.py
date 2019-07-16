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

from vehicles.models import ServiceTrackingArea, SubUrb, PublicTransportStation


class Command(BaseCommand):

    help = 'searches for routes in the dataset for today'

    def add_arguments(self, parser):
        parser.add_argument('service_area', type=int)

    def handle(self, *args, **options):

        service_area = ServiceTrackingArea.objects.get(id=options["service_area"])
        bbox = Polygon(wkt.loads(str(service_area.area).split(";")[1])).convex_hull
        print(bbox.bounds)
        overpass_query = f"""
        [out:json];
        node
            ["railway"~"subway_entrance|station"]
          ({bbox.bounds[1]},{bbox.bounds[0]},{bbox.bounds[3]},{bbox.bounds[2]});
        out;
        """
        api = overpy.Overpass()
        result = api.query(overpass_query)
        for node in result.nodes:
            PublicTransportStation.objects.create(position=Point([node.lon, node.lat]),
                                                  name=node.tags["name"] if "name" in node.tags else "",
                                                  service_area=service_area
                                                  )
            print(node.tags["name"] if "name" in node.tags else "")