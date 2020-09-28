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

from vehicles.models import ServiceTrackingArea, Vehicle, VehicleLocationTrack, SubUrb
from vehicles.services import PublicTransportService


def import_crawler(name):
    path_parts = name.split(".")
    cls = path_parts[-1]
    del path_parts[-1]
    lib = ".".join(path_parts)
    module = importlib.import_module(lib)
    return getattr(module, cls)


def filter_location_vehicles(vehicles, area):
    vhs =[]
    for vehicle in vehicles:
        if Point(vehicle.lon, vehicle.lat).within(area):
            vhs.append(vehicle)

    return vhs


def save_to_db(vehicles, service_provider):
    for vehicle in vehicles:

        try:
            db_v, created = Vehicle.objects.get_or_create(service_provider=service_provider,
                                                          vehicle_id=vehicle.vehicle_id,
                                                          vehicle_type=vehicle.vehicle_type)
            vt = VehicleLocationTrack.objects.create(vehicle=db_v, position=vehicle.location, raw_data=vehicle.raw_data,
                                            battery_level=vehicle.battery_level, last_seen=vehicle.last_seen,
                                            suburb=SubUrb.objects.filter(area__contains=vehicle.location).first())
        except Exception as e:
            print(e)

class Command(BaseCommand):

    help = 'executes the configured crawlers'

    def handle(self, *args, **options):

        for service_area in ServiceTrackingArea.objects.all():
            for service in service_area.service_providers.all():
                print(service)
                crawler_cls = import_crawler(service.crawler)
                crawler = crawler_cls(service.settings)
                print(crawler)
                if not crawler.LOCATION_BASED_CRAWLING:
                    ctr = Polygon(wkt.loads(str(service_area.area).split(";")[1])).centroid
                    vehicles = crawler.nearby_search(ctr.y, ctr.x, service_provider=service, service_area=service_area)
                    f_vehicles = filter_location_vehicles(
                        vehicles, Polygon(wkt.loads(str(service_area.area).split(";")[1])))
                    save_to_db(f_vehicles, service)
                else:
                    shp = Polygon(wkt.loads(str(service_area.area).split(";")[1])).convex_hull
                    print(shp)
                    top_left_x = shp.bounds[0]
                    top_left_y = shp.bounds[1]
                    radius = 1400

                    buffer = (radius / 40000000. * 360. / math.cos(top_left_y / 360. * math.pi))

                    top_left_y += buffer
                    top_left_x += buffer

                    curr_x = top_left_x
                    curr_y = top_left_y
                    points = []

                    while Point(curr_x, curr_y).within(shp):

                        while Point(curr_x, curr_y).within(shp):
                            print(Point(curr_x, curr_y))
                            points.append(Point(curr_x, curr_y))
                            curr_y += (buffer * 2)

                        curr_y = top_left_y
                        curr_x += buffer

                    vehicles = {}

                    for p in points:
                        crwl_result = crawler.nearby_search(p.y, p.x, radius=radius, service_provider=service,
                                                            service_area=service_area)
                        for v in crwl_result:
                            vehicles[v.vehicle_id] = v
                        print(len(vehicles))

                    f_vehicles = filter_location_vehicles(
                        [v for k, v in vehicles.items()], Polygon(wkt.loads(str(service_area.area).split(";")[1])))
                    save_to_db(f_vehicles, service)
