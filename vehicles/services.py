import json
import operator
from datetime import datetime, timedelta, time
from enum import Enum
from functools import reduce

import requests
from django.conf import settings
from django.contrib.gis.measure import Distance
from django.db.models import Avg, Count, Sum, F, Q
from django.db.models.functions import ExtractWeekDay
from serious_django_enums import AutoEnum
from serious_django_services import Service
from vehicles.models import ServiceTrackingArea, Pricing, VehicleLocationTrack, Vehicle, TripEstimation, \
    ServiceProvider, SubUrb, PublicTransportStation


class PriceEstimationService(Service):

    service_exceptions = ()

    @classmethod
    def calculate_price(cls, start: VehicleLocationTrack, end: VehicleLocationTrack) -> float:
        area = ServiceTrackingArea.objects.filter(area__contains=start.position).first()
        try:
            pricing = Pricing.objects.get(service_provider=start.vehicle.service_provider, service_area=area)
        except Pricing.DoesNotExist:
            return None

        return pricing.unlock_fee + int((end.last_seen - start.last_seen).total_seconds()/60) * pricing.minute_price


class RouteEstimationService(Service):
    service_exceptions = ()

    @classmethod
    def get_routing(cls, start_point: [float, float], end_point: [float, float]):
        """get informations like distance, time and geojson for the calculated route"""
        # no I'm not drunk but the people behind the graphhopper api might have been when they built it
        routing_coords = [",".join([str(itm) for itm in reversed(start_point)])]

        routing_coords.append(
            ",".join([str(itm) for itm in reversed(end_point)]))

        routing_request = {
            "key": settings.GRAPH_HOPPER_APIKEY,
            "vehicle": "bike",
            "point": routing_coords,
            "locale": "de",
            "details": "time",
            "points_encoded": False,
            "instructions": False
        }
        response = requests.get("https://graphhopper.com/api/1/route", params=routing_request)
        print(response.json())
        return response.json()


class StatisticAggregationService(Service):

    service_exceptions = ()

    @classmethod
    def get_latest_geojson(cls):
        geojson_list = []

        color_mapping = { "voi": "#f46c62", "lime": "#24d000", "tier": "#69d2aa", "circ": "#f56600"}


        for itm in VehicleLocationTrack.objects\
                .filter(updated_at__gte=datetime.now()-timedelta(hours=2)).distinct('vehicle'):

                geojson_list.append({
                    "type": "Feature",
                    "properties": {
                        "color": color_mapping[itm.vehicle_id.split("-")[0]] if itm.vehicle_id.split("-")[0] in color_mapping else "#000"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [itm.position.x, itm.position.y]
                    }
                })

        return [{"geojson": json.dumps({
            "type": "FeatureCollection",
            "features": geojson_list
        })}]


    @classmethod
    def calculate_avg_trips(cls, queryset=None):

        service_providers = []

        if not queryset:
            queryset = TripEstimation.objects.filter(updated_at__gte=datetime.now() - timedelta(hours=12))

        for sp in queryset.values('vehicle__service_provider') \
                .annotate(avg_duration=Avg('duration'),
                          avg_price=Avg('price_estimation'),
                          avg_distance=Avg('route_distance_estimation'),
                          count_trips=Count('id'),
                          ):
            sp_ = ServiceProvider.objects.get(id=sp["vehicle__service_provider"])
            seen_vehicles = VehicleLocationTrack.objects \
                .filter(updated_at__gte=datetime.now() - timedelta(hours=1)) \
                .filter(vehicle__service_provider=sp_).distinct('vehicle_id').count()
            service_providers.append({"service_provider": sp_,
                                      "average_price":float(sp["avg_price"]),
                                      "count_scooters": seen_vehicles,
                                      "count_trips": sp["count_trips"],
                                      "average_distance": int(sp["avg_distance"]),
                                      "average_duration":sp["avg_duration"].seconds//60})


        return service_providers

    @classmethod
    def get_trip_type_stats(cls, queryset=None):

        if not queryset:
            queryset = TripEstimation.objects.filter(updated_at__gte=datetime.now() - timedelta(hours=12))

        trip_types = []
        for tp in queryset.values('trip_type') \
                .annotate(Count("trip_type"),
                          scooter_count_nearby_station=Count('trip_type',
                                                             filter=(~Q(started_at_station=None)|~Q(
                                                                 ended_at_station=None)))):
            print(tp)
            trip_types.append({
                'name': tp["trip_type"],
                'count': tp["trip_type__count"],
                'count_nearby_station': tp["scooter_count_nearby_station"]
                 })
        print(trip_types)
        return trip_types


    @classmethod
    def trip_week_stats(cls, queryset=None):

        if not queryset:
            queryset = TripEstimation.objects.filter(updated_at__gte=datetime.now() - timedelta(hours=24))

        week_stats = []
        for tp in queryset.values('trip_type') \
                .extra({'hour': 'strftime("%%H", start_point__last_seen)'})\
                .annotate(weekday=ExtractWeekDay('start_point__last_seen'))\
                .values('weekday', 'start_point__last_seen__hour')\
                .annotate(Count('id')):
            week_stats.append({
                'weekday': (tp["weekday"]+5)%7,
                'hour': tp["start_point__last_seen__hour"],
                'count': tp["id__count"],
            })


        return week_stats


    @classmethod
    def get_suburb_stats(cls):

        scooter_suburbs = []

        for t in VehicleLocationTrack.objects.values('suburb__id', 'suburb__name') \
                .filter(id__in=VehicleLocationTrack.objects.values('id')
                .filter(updated_at__gte=datetime.now() - timedelta(hours=12)).distinct('vehicle')) \
                .annotate(scooter_count=Count('suburb__id')):
            scooter_suburbs.append(t)

        scooters = SubUrb.objects.filter(
            id__in=[i["suburb__id"] for i in scooter_suburbs])\
            .aggregate(
            avg_i=Avg('avg_income'),
            sum_p=Sum('population'),
            weighted_avg_i=Sum(F('avg_income') * F('population')),
            count=Count('id')
        )


        without_scooters = SubUrb.objects.exclude(
            id__in=[i["suburb__id"] for i in scooter_suburbs if i["suburb__id"]])\
            .aggregate(
                avg_i=Avg('avg_income'),
                sum_p=Sum('population'),
                weighted_avg_i=Sum(F('avg_income') * F('population')),
                count=Count('id')
            )

        print(scooters)
        return [{
            "suburbs_without_scooter_average_income": int(without_scooters["weighted_avg_i"]/without_scooters["sum_p"]),
            "suburbs_without_scooter_population":without_scooters["sum_p"],
            "suburbs_without_scooter_count":without_scooters["count"],
            "suburbs_with_scooter_average_income":int(scooters["weighted_avg_i"]/scooters["sum_p"]),
            "suburbs_with_scooter_population":scooters["sum_p"],
            "suburbs_with_scooter_count":scooters["count"],
        }]






class PublicTransportService(Service):
    service_exceptions = ()

    @classmethod
    def assign_station_to_track(cls, track):

        station = PublicTransportStation.objects.filter(position__distance_lt=(track.position, Distance(km=0.04))).first()
        if station:
            track.public_transport_station = station
            track.save()
        else:
            track.public_transport_station = None
            track.save()


    @classmethod
    def assign_station_to_trip_estimation(cls, trip_estimation):

        station = PublicTransportStation.objects.filter(position__distance_lt=(trip_estimation.start_point.position, Distance(km=0.05))).first()
        if station:
            trip_estimation.started_at_station= station
            trip_estimation.save()
        else:
            trip_estimation.started_at_station = None
            trip_estimation.save()


        station = PublicTransportStation.objects.filter(
            position__distance_lt=(trip_estimation.end_point.position, Distance(km=0.03))).first()
        if station:
            trip_estimation.ended_at_station = station
            trip_estimation.save()
        else:
            trip_estimation.ended_at_station = None
            trip_estimation.save()




class DayTimeFrame(Enum):
    ALL_DAY = 'ALL_DAY'
    MORNING = 'MORNING'
    FORENOON = 'FORENOON'
    NOON = 'NOON'
    AFTERNOON = 'AFTERNOON'
    EVENING = 'EVENING'

class TimeFrame(Enum):
    ALL_TIME = 'ALL_TIME'
    TODAY = 'TODAY'
    THIS_WEEK = 'WEEK'
    THIS_MONTH = 'MONTH'

class TripType(Enum):
    ALL = 'ALL'
    SHORT = 'SHORT_TRIP'
    LONG = 'LONG_TRIP'
    FUN = 'FUN_TRIP'


class DataExplorationService(Service):
    service_exceptions = ()


    @classmethod
    def query_filter(cls, trip_type=TripType.ALL, started_at_station=None, ended_at_station=None,
                     group_rides=None, day_time_frame=DayTimeFrame.ALL_DAY, time_frame=TimeFrame.TODAY):


        qs = TripEstimation.objects

        filters = []


        if trip_type != TripType.ALL.name:
            filters.append(Q(trip_type=trip_type))


        if DayTimeFrame.MORNING.name == day_time_frame:
            filters.append(Q(start_point__last_seen__time__gte=time(6,0),
                             start_point__last_seen__time__lte=time(10,0)))
        elif DayTimeFrame.FORENOON.name == day_time_frame:
            filters.append(Q(start_point__last_seen__time__gte=time(9, 0),
                             start_point__last_seen__time__lte=time(12, 0)))
        elif DayTimeFrame.NOON.name == day_time_frame:
            filters.append(Q(start_point__last_seen__time__gte=time(9, 0),
                             start_point__last_seen__time__lte=time(12, 0)))
        elif DayTimeFrame.AFTERNOON.name == day_time_frame:
            filters.append(Q(start_point__last_seen__time__gte=time(14, 0),
                            start_point__last_seen__time__lte=time(18, 0)))
        elif DayTimeFrame.EVENING.name == day_time_frame:
            filters.append(Q(start_point__last_seen__time__gte=time(18, 0),
                             start_point__last_seen__time__lte=time(23, 30)))

        if time_frame == TimeFrame.TODAY.name:
            filters.append(Q(updated_at__gte=datetime.now()-timedelta(hours=24)))
        elif time_frame == TimeFrame.THIS_WEEK.name:
            filters.append(Q(updated_at__gte=datetime.now() - timedelta(days=7)))
        elif time_frame == TimeFrame.THIS_MONTH.name:
            filters.append(Q(updated_at__gte=datetime.now() - timedelta(days=30)))


        if started_at_station == True:
            filters.append(~Q(started_at_station=None))
        elif started_at_station == False:
            filters.append(Q(started_at_station=None))

        if ended_at_station == True:
            filters.append(~Q(ended_at_station=None))
        elif ended_at_station == False:
            filters.append(Q(ended_at_station=None))
        print(Q(*filters))
        return qs.filter(Q(*filters))
