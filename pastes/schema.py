from graphene import relay

from graphene.contrib.django.types import DjangoNode

from .models import Paste


class PasteNode(DjangoNode):
    node = relay.NodeField()

    class Meta:
        model = Paste
