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
