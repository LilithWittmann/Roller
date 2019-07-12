from vehicles.crawlers.fleetbird import FleetbirdCrawler


class EmmyCrawler(FleetbirdCrawler):

    SERVICE_PROVIDER = "emmy"

    def __init__(self, settings: dict):
        settings["INSTANCE_NAME"] = "emmy"
        settings["PROVIDER_NAME"] = "emmy"
        super().__init__(settings)
