from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models
from serious_django_enums import AutoEnum

CRAWLER_CHOICES = ((cls,name) for name, cls in settings.INSTALLED_CRAWLERS.items())


class ServiceProvider(models.Model):
    name = models.CharField(max_length=30)
    crawler = models.CharField(max_length=50, choices=CRAWLER_CHOICES, null=True)
    primary_color = models.CharField(max_length=7, null=True)
    text_color = models.CharField(max_length=7, null=True)
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


class SubUrb(gis_models.Model):
    name = models.CharField(max_length=100)
    population = models.BigIntegerField(null=True)
    avg_income = models.BigIntegerField(null=True)
    area = gis_models.PolygonField()
    service_area = models.ForeignKey(ServiceTrackingArea, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.population}, {self.avg_income})'


class Pricing(models.Model):
    service_area = models.ForeignKey(ServiceTrackingArea, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)

    unlock_fee = models.DecimalField(decimal_places=3, max_digits=5)
    minute_price = models.DecimalField(decimal_places=3, max_digits=5)

    free_minutes = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f'{self.service_provider} {self.service_area}'


class Vehicle(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, related_name="vehicles", on_delete=models.CASCADE)
    vehicle_id = models.CharField(max_length=200, primary_key=True, editable=False)

    @property
    def last_track(self):
        return self.location_track.order_by('-updated_at').first()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle_id'], name="unique-vehicle-id"),
        ]

    def __str__(self):
        return self.vehicle_id



class PublicTransportStation(models.Model):
    name = models.CharField(max_length=255)
    position = gis_models.PointField(srid=4326)
    service_area = models.ForeignKey(ServiceTrackingArea, related_name='stations', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class VehicleLocationTrack(gis_models.Model):

    vehicle = models.ForeignKey(Vehicle, related_name="location_track", on_delete=models.CASCADE)
    suburb = models.ForeignKey(SubUrb, related_name="tracks", null=True, on_delete=models.SET_NULL)
    public_transport_station = models.ForeignKey(PublicTransportStation,
                                                 related_name="tracks",null=True, on_delete=models.SET_NULL)
    position = gis_models.PointField(null=True, blank=True, srid=4326)
    battery_level = models.IntegerField(null=True)
    last_seen = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at_day = models.DateField(null=True, auto_now_add=True)
    raw_data = models.TextField()

    @property
    def position_geojson(self):
        return self.position.geojson


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'last_seen'], name="unique-user-short-ref"),
            models.UniqueConstraint(fields=['vehicle', 'position', 'battery_level', 'updated_at_day'], name="unique-vehicle-position-battery"),
        ]
        indexes = [
            models.Index(fields=['vehicle']),
            models.Index(fields=['vehicle', 'updated_at'])
        ]


    def __str__(self):
        return self.vehicle.vehicle_id

class TripTypes(AutoEnum):
    choices = (
        ('SHORT_TRIP', 'short area trip; usually less than 5km'),
        ('LONG_TRIP', 'long trips; usually more than 5km'),
        ('FUN_TRIP', 'a trip that probably just out of curiosity or by tourists'),
        ('UNCLASSIFIED', 'not classified'),
        ('DEPLOYMENT', 'deployment of scooter'),
        ('UNKNOWN', 'hmm?!'),
    )

class TripEstimation(gis_models.Model):
    start_point = models.ForeignKey(VehicleLocationTrack, related_name="route_start", on_delete=models.CASCADE)
    end_point = models.ForeignKey(VehicleLocationTrack, related_name="route_end", on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, related_name="trips", on_delete=models.CASCADE)
    price_estimation = models.DecimalField(decimal_places=3, max_digits=7, null=True)
    route_estimation = gis_models.LineStringField(null=True)
    route_duration_estimation = models.DurationField(null=True)
    route_distance_estimation = models.IntegerField(null=True)
    started_at_station = models.ForeignKey(PublicTransportStation, related_name="started_trips",
                                           null=True, on_delete=models.SET_NULL)
    ended_at_station = models.ForeignKey(PublicTransportStation, related_name="ended_trips",
                                           null=True, on_delete=models.SET_NULL)
    route_timing = JSONField(
        verbose_name='route timing',
        null=True,
        blank=True
    )
    duration = models.DurationField()
    trip_type = models.CharField(choices=TripTypes.choices, max_length=100, default=TripTypes.UNCLASSIFIED)
    updated_at = models.DateTimeField(null=True, auto_now_add=True)



    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['start_point'], name="unique-start"),
            models.UniqueConstraint(fields=['end_point'], name="unique-end"),
        ]
        indexes = [
            models.Index(fields=['vehicle']),
            models.Index(fields=['vehicle', 'updated_at'])
        ]


    @property
    def start_position(self):
        return self.start_point.position

    @property
    def end_position(self):
        return self.end_point.position

    @property
    def battery_consumption(self):
        return (self.start_point.battery_level - self.end_point.battery_level) if self.start_point.battery_level else 0

    def __str__(self):
        return f'{self.vehicle} ({self.duration} minutes)'
