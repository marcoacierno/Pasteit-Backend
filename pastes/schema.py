import graphene

from graphene import relay

from graphene.contrib.django.types import DjangoNode

from .models import Paste


class PasteNode(DjangoNode):
    node = relay.NodeField()
    owner = graphene.Field('ProfileNode')

    class Meta:
        model = Paste


class Query(graphene.ObjectType):
    pastes = relay.ConnectionField(PasteNode)

    def resolve_pastes(self, args, info):
        return Paste.objects.filter(visibility=Paste.VISIBILITY[0][0]).all()
