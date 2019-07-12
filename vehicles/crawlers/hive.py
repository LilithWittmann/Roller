from vehicles.crawlers.fleetbird import FleetbirdCrawler


class HiveCrawler(FleetbirdCrawler):

    SERVICE_PROVIDER = "hive"

    def __init__(self, settings: dict):
        settings["INSTANCE_NAME"] = "hive"
        settings["PROVIDER_NAME"] = "hive"
        super().__init__(settings)
