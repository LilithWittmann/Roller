from django.apps import AppConfig


class VehiclesConfig(AppConfig):
    name = 'vehicles'

    def register_signals(self):
        from . import signals

    def ready(self):
        self.register_signals()
