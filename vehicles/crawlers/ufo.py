from vehicles.crawlers.fleetbird import FleetbirdCrawler

class UfoCrawler(FleetbirdCrawler):


    SERVICE_PROVIDER = "ufo"

    def __init__(self, settings: dict):
        settings["INSTANCE_NAME"] = "ufo"
        settings["PROVIDER_NAME"] = "ufo"
        super().__init__(settings)
