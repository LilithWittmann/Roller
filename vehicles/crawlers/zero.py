from vehicles.crawlers.fleetbird import FleetbirdCrawler


class ZeroCrawler(FleetbirdCrawler):


    SERVICE_PROVIDER = "zero"

    def __init__(self, settings: dict):
        settings["INSTANCE_NAME"] = "zero"
        settings["PROVIDER_NAME"] = "zero"
        super().__init__(settings)
