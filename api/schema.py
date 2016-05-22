import graphene

import profiles.schema
import pastes.schema

from profiles.schema import UserNode, ProfileNode
from pastes.schema import PasteNode


class Query(profiles.schema.Query, pastes.schema.Query):
    pass


schema = graphene.Schema(name='Pasteit API')

schema.register(UserNode)
schema.register(PasteNode)
schema.register(ProfileNode)

schema.query = Query
