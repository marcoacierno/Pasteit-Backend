import graphene

import profiles.schema
import pastes.schema

from profiles.schema import UserNode
from pastes.nodes import PasteNode


class Query(profiles.schema.Query, pastes.schema.Query):
    pass


class Mutations(pastes.schema.Mutation):
    pass


schema = graphene.Schema(name='Pasteit API')

schema.register(UserNode)
schema.register(PasteNode)

schema.query = Query
schema.mutation = Mutations
