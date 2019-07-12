from vehicles.crawlers.fleetbird import FleetbirdCrawler


class HiveCrawler(FleetbirdCrawler):

    def __init__(self, settings: dict):
        settings["INSTANCE_NAME"] = "hive"
        settings["PROVIDER_NAME"] = "hive"
        super().__init__(settings)
