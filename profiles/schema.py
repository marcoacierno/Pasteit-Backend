import graphene

from graphene import relay


class Query(graphene.ObjectType):
    node = relay.NodeField()

    class Meta:
        abstract = True
