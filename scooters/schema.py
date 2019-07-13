import graphene

# Import your app's schemas like:
#
# import subappA.schema
# import subappB.schema
#
# - and then have Query and Mutation below inherit from them.

from vehicles import  schema as vehicle_schema

class Query(
    # TODO put query classes from your apps here

    vehicle_schema.Query,
    graphene.ObjectType,
):
    # This class will inherit from multiple Queries as we add apps to our project
    pass


class Mutation(
    # TODO put mutation classes from your apps here

    #vehicle_schema.Mutation,
    graphene.ObjectType
):
    # This class will inherit from multiple Mutations as we add apps to our project
    pass

# TODO: as soon as you've defined your Query and Mutation, add
# `query=Query` and/or `mutation=Mutation`
# to the constructor call below.
schema = graphene.Schema(
    query=Query,
    #mutation=Mutation
)
