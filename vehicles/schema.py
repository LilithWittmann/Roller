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


## Queries

class Query(graphene.ObjectType):
    """
    This class includes all available queries for this app.
    """
    pass
    # EXAMPLE:
    # some_field = graphene.Field(
    #    ...
    # )
    # def resolve_some_field(root, info):
    #     user = get_user_from_info(info)
    #     ...


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

schema = graphene.Schema(query=Query, mutation=Mutation)
