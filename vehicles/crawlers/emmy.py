from vehicles.crawlers.fleetbird import FleetbirdCrawler


class EmmyCrawler(FleetbirdCrawler):

    SERVICE_PROVIDER = "emmy"
    VEHICLE_TYPE = "emoped"

    def __init__(self, settings: dict):
        settings["INSTANCE_NAME"] = "emmy"
        settings["PROVIDER_NAME"] = "emmy"
        super().__init__(settings)
