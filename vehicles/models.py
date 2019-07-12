from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models



CRAWLER_CHOICES = ((cls,name) for name, cls in settings.INSTALLED_CRAWLERS.items())


class ServiceProvider(models.Model):
    name = models.CharField(max_length=30)
    crawler = models.CharField(max_length=50, choices=CRAWLER_CHOICES, null=True)
    settings = JSONField(
        verbose_name='configuration attributes'
    )
    def __str__(self):
        return self.name


class ServiceTrackingArea(gis_models.Model):
    name = models.CharField(max_length=30)
    area = gis_models.PolygonField()
    service_providers = models.ManyToManyField(ServiceProvider)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, related_name="vehicles", on_delete=models.CASCADE)
    vehicle_id = models.CharField(max_length=200)

    def __str__(self):
        return self.vehicle_id


class VehicleLocationTrack(gis_models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="location_track", on_delete=models.CASCADE)
    position = gis_models.PointField(null=True, blank=True, srid=4326)
    battery_level = models.IntegerField(null=True)
    last_seen = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    raw_data = models.TextField()

    def __str__(self):
        return self.vehicle.vehicle_id


class TripEstimation(models.Model):
    start_point = models.ForeignKey(VehicleLocationTrack, related_name="route_start", on_delete=models.CASCADE)
    end_point = models.ForeignKey(VehicleLocationTrack, related_name="route_end", on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, related_name="trips", on_delete=models.CASCADE)
    duration = models.DurationField()
