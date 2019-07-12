import math

from django.test import TestCase
from django.conf import settings

from vehicles.crawlers.circ import CircCrawler
from vehicles.crawlers.emmy import EmmyCrawler
from vehicles.crawlers.hive import HiveCrawler
from vehicles.crawlers.lime import LimeCrawler
from vehicles.crawlers.tier import TierCrawler
from vehicles.crawlers.ufo import UfoCrawler
from vehicles.crawlers.voi import VoiCrawler
from vehicles.crawlers.zero import ZeroCrawler


class TestTier(TestCase):
    def test_crawling(self):
        # its everywhere on the internet…
        crawler = TierCrawler({"API_KEY": "bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2"})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        self.assertLess(1, len(vehicles))


class TestVoi(TestCase):
    def test_crawling(self):
        crawler = VoiCrawler({})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        print(len(vehicles))
        self.assertLess(1, len(vehicles))


class TestLime(TestCase):
    def test_crawling(self):
        crawler = LimeCrawler({"AUTHORIZATION": settings.LIME_AUTHORIZATION,
                               "WEB_SESSION": settings.LIME_SESSION})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        print(len(vehicles))
        for vehicle in vehicles:
            print(vehicle.vehicle_id)
            print(vehicle.lat)

        self.assertLess(1, len(vehicles))


class TestCirc(TestCase):
    def test_crawling(self):
        crawler = CircCrawler({})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        print(len(vehicles))
        for vehicle in vehicles:
            print(vehicle.vehicle_id)
            print(vehicle.lat)

        self.assertLess(1, len(vehicles))


class TestHive(TestCase):
    def test_crawling(self):
        crawler = HiveCrawler({})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        self.assertLess(1, len(vehicles))
        print(len(vehicles))


class TestEmmy(TestCase):
    def test_crawling(self):
        crawler = EmmyCrawler({})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        self.assertLess(1, len(vehicles))
        print(len(vehicles))


class TestZero(TestCase):
    def test_crawling(self):
        crawler = ZeroCrawler({})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        self.assertLess(1, len(vehicles))
        print(len(vehicles))


class TestUfo(TestCase):
    def test_crawling(self):
        crawler = UfoCrawler({})
        vehicles = crawler.nearby_search(53.546723, 9.995547)
        self.assertLess(1, len(vehicles))
        print(len(vehicles))




class TestCalculation(TestCase):
    def test_crawling(self):
        from shapely.geometry import shape, Point
        import geojson
        import json

        shp = shape({
        "type": "Polygon",
        "coordinates": [
          [
            [
              9.909324645996112,
              53.53969532109345
            ],
            [
              10.078926086425799,
              53.535002487312106
            ],
            [
              10.076522827148438,
              53.60432183675507
            ],
            [
              9.96425628662111,
              53.608803292930865
            ],
            [
              9.906921386718766,
              53.60941436374625
            ],
            [
              9.909324645996112,
              53.53969532109345
            ]
          ]
        ]
      })

        top_left_x = shp.convex_hull.bounds[0]
        top_left_y = shp.convex_hull.bounds[1]
        radius = 900

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
                curr_y += (buffer*2)

            curr_y = top_left_y
            curr_x += buffer

        geojson = []
        print(len(points))
        vehicles = {}
        for p in points:
            crawler = TierCrawler({"API_KEY": "bpEUTJEBTf74oGRWxaIcW7aeZMzDDODe1yBoSxi2"})
            crwl_result = crawler.nearby_search(p.y,p.x, radius=500)

            for v in crwl_result:
                vehicles[v.vehicle_id] = v
            print(len(vehicles))

        print(json.dumps(geojson))

