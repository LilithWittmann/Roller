from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models



class ServiceProvider(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, related_name="vehicles", on_delete=models.CASCADE)
    vehicle_id = models.CharField(max_length=200)


class VehicleLocationTrack(gis_models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="location_track", on_delete=models.CASCADE)
    position = gis_models.PointField(null=True, blank=True, srid=4326)
    battery_level = models.IntegerField(null=True)
    raw_data = models.TextField()


class TripEstimation(models.Model):
    start_point = models.ForeignKey(VehicleLocationTrack, related_name="route_start", on_delete=models.CASCADE)
    end_point = models.ForeignKey(VehicleLocationTrack, related_name="route_end", on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, related_name="trips", on_delete=models.CASCADE)
    duration = models.DurationField()