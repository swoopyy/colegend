import graphene
from graphene_django.debug import DjangoDebug

import colegend.users.schema
import colegend.office.schema
import colegend.outcomes.schema
from colegend.checkpoints.schema import CheckpointQuery, CheckpointMutation
from colegend.community.schema import CommunityQuery, CommunityMutation
from colegend.home.schema import HomeQuery, HomeMutation
from colegend.journey.schema import JourneyQuery, JourneyMutation


class Query(
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    colegend.users.schema.UserQuery,
    CheckpointQuery,
    HomeQuery,
    JourneyQuery,
    colegend.office.schema.FocusQuery,
    colegend.outcomes.schema.OutcomeQuery,
    CommunityQuery,
    graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
    colegend.users.schema.UserMutation,
    CheckpointMutation,
    HomeMutation,
    JourneyMutation,
    CommunityMutation,
    graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
