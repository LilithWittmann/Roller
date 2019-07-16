from abc import ABC, abstractmethod

import graphene
from graphene_django.types import DjangoObjectType

from graphene_gis_extension import\
    scalars as gis_scalars,\
    input_types as gis_input_types

from serious_django_graphene import get_user_from_info, \
    FormMutation, MutationExecutionException, MutationError

# Import your Services (and maybe Forms) here.


## Types
# Define your Graphene types here. For types corresponding to Django models,
# use DjangoObjectType:
# http://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/#hello-graphql-schema-and-object-types
from serious_django_services import NotPassed

from vehicles.models import Vehicle, ServiceProvider, VehicleLocationTrack
from vehicles.services import StatisticAggregationService, TripType, DayTimeFrame, TimeFrame, DataExplorationService


class VehicleLocationTrackType(DjangoObjectType):
    position_geojson = graphene.String()

    def resolve_position_geojson(self, info, **kwargs):
        return self.position_geojson

    class Meta:
        model = VehicleLocationTrack

class ServiceProviderType(DjangoObjectType):
    class Meta:
        model = ServiceProvider

class VehicleType(DjangoObjectType):
    last_track = graphene.Field(VehicleLocationTrackType)


    class Meta:
        model = Vehicle



class LatestMapType(graphene.ObjectType):
    geojson = graphene.String()


class DayStatsType(graphene.ObjectType):
    average_price = graphene.Float()
    count_trips = graphene.Int()
    count_scooters = graphene.Int()
    average_duration = graphene.Float()
    average_distance = graphene.Float()
    service_provider = graphene.Field(ServiceProviderType)


class SuburbStats(graphene.ObjectType):
    suburbs_without_scooter_average_income = graphene.Int()
    suburbs_without_scooter_population = graphene.Int()
    suburbs_without_scooter_count = graphene.Int()
    suburbs_with_scooter_average_income = graphene.Int()
    suburbs_with_scooter_population = graphene.Int()
    suburbs_with_scooter_count = graphene.Int()


class TripTypeAggregation(graphene.ObjectType):
    count = graphene.Int()
    count_nearby_station = graphene.Int()
    name = graphene.String()


class TripsWeekAggregation(graphene.ObjectType):
    count = graphene.Int()
    hour = graphene.Int()
    weekday = graphene.Int()



## Queries

class Query(graphene.ObjectType):
    """
    This class includes all available queries for this app.
    """
    all_vehicles = graphene.List(VehicleType)
    latest_map = graphene.List(LatestMapType)
    all_service_provider = graphene.List(ServiceProviderType)
    day_stats = graphene.List(DayStatsType)
    suburb_stats = graphene.List(SuburbStats)
    trip_types = graphene.List(TripTypeAggregation)

    def resolve_all_vehicles(self, info, **kwargs):
        return Vehicle.objects.all()

    def resolve_all_service_provider(self, info, **kwargs):
        return ServiceProvider.objects.all()

    def resolve_suburb_stats(self, info, **kwargs):
        return StatisticAggregationService.get_suburb_stats()

    def resolve_latest_map(self, info, **kwargs):
        return StatisticAggregationService.get_latest_geojson()


    def resolve_day_stats(self, info, **kwargs):
        return StatisticAggregationService.calculate_avg_trips()

    def resolve_trip_types(self, info, **kwargs):
        return StatisticAggregationService.get_trip_type_stats()

from six import with_metaclass


class DataExplorerMutation(graphene.Mutation):

    class Arguments:
        started_at_station = graphene.Boolean()
        ended_at_station = graphene.Boolean()
        day_time_frame = graphene.Enum.from_enum(DayTimeFrame)(required=True)
        trip_type = graphene.Enum.from_enum(TripType)(required=True)
        time_frame = graphene.Enum.from_enum(TimeFrame)(required=True)

    class Meta:
        abstract = True

    success = graphene.Boolean()
    error = MutationError()

    @classmethod
    def process_query(cls, qs):
        raise NotImplementedError(
            "process_query needs to be overridden in the subclass!"
        )

    @classmethod
    def mutate(cls, root, info, trip_type=NotPassed, day_time_frame=NotPassed, time_frame=NotPassed,
               ended_at_station=NotPassed, started_at_station=NotPassed):
        query_data = {}
        if trip_type != NotPassed:
            query_data['trip_type'] = trip_type
        if day_time_frame != NotPassed:
            query_data['day_time_frame'] = day_time_frame
        if ended_at_station != NotPassed:
            query_data['ended_at_station'] = ended_at_station
        if started_at_station != NotPassed:
            query_data['started_at_station'] = started_at_station
        if time_frame != NotPassed:
            query_data['time_frame'] = time_frame


        try:
            print(query_data)
            query = DataExplorationService.query_filter(**query_data)
        except DataExplorationService.exceptions as e:
            raise MutationExecutionException(str(e))

        return cls.process_query(query)



class TripTypeStatsMutation(DataExplorerMutation):

    @classmethod
    def process_query(cls, qs):
        return {"result": StatisticAggregationService.get_trip_type_stats(qs)}

    result = graphene.List(TripTypeAggregation)


class TripsWeekStatsMutation(DataExplorerMutation):

    @classmethod
    def process_query(cls, qs):
        return {"result": StatisticAggregationService.trip_week_stats(qs)}

    result = graphene.List(TripsWeekAggregation)



class Mutation(graphene.ObjectType):
    exploreTripTypeStats = TripTypeStatsMutation.Field(name="exploreTripTypeStats",
                                                       description="Explore different trip types")
    tripWeekStats = TripsWeekStatsMutation.Field(name="exploreTripsOverWeek",
                                                       description="Explore trip  distribution over time")

## Schema

schema = graphene.Schema(query=Query, mutation=Mutation)
