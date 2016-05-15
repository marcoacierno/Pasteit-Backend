import graphene

import profiles.schema

from graphene.contrib.django.debug import DjangoDebugPlugin


class Query(profiles.schema.Query):
    pass

schema = graphene.Schema(name='Pasteit API', plugins=[DjangoDebugPlugin()])
schema.query = Query
