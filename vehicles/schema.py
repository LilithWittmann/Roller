import graphene
from graphene_django.types import DjangoObjectType

from graphene_gis_extension import\
    scalars as gis_scalars,\
    input_types as gis_input_types

from serious_django_graphene import get_user_from_info,\
    FormMutation, MutationExecutionException

# Import your Services (and maybe Forms) here.


## Types
# Define your Graphene types here. For types corresponding to Django models,
# use DjangoObjectType:
# http://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/#hello-graphql-schema-and-object-types
from vehicles.models import Vehicle, ServiceProvider, VehicleLocationTrack
from vehicles.services import VehicleService


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

## Queries

class Query(graphene.ObjectType):
    """
    This class includes all available queries for this app.
    """
    all_vehicles = graphene.List(VehicleType)
    latest_map = graphene.List(LatestMapType)
    all_service_provider = graphene.List(ServiceProviderType)

    def resolve_all_vehicles(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Vehicle.objects.all()

    def resolve_all_service_provider(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return ServiceProvider.objects.all()


    def resolve_latest_map(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return VehicleService.get_latest_geojson()

## Mutations

# EXAMPLE:
# class SomeFormBasedMutation(FormMutation):
#    class Meta:
#        form_class = SomeForm

#    @classmethod
#    def perform_mutate(cls, form, info):
#        user = get_user_from_info(info)
#        data = form.cleaned_data
#        try:
#            SomeService.do_something(user, data)
#        except SomeService.exceptions as e:
#            raise MutationExecutionException(str(e))
#        return cls(...)


class Mutation(graphene.ObjectType):
    # some_mutation = SomeFormBasedMutation.Field(name=..., description=...)
    pass


## Schema

schema = graphene.Schema(query=Query)
                         #, mutation=Mutation)
