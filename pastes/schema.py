import graphene

from graphene.contrib.django.filter.fields import DjangoFilterConnectionField

from .models import Paste

from .nodes import PasteNode
from .mutations import CreatePaste


class Query(graphene.ObjectType):
    pastes = DjangoFilterConnectionField(PasteNode)
    paste = graphene.Field(PasteNode, hash_id=graphene.String())

    def resolve_paste(self, args, info):
        hash_id = args.get('hash_id', None)

        if not hash_id:
            return None

        try:
            return Paste.objects.get(hash_id=hash_id)
        except Paste.DoesNotExist:
            return None

    def resolve_pastes(self, args, info):
        return Paste.objects.filter(visibility=Paste.VISIBILITY[0][0]).all()


class Mutation(graphene.ObjectType):
    create_paste = graphene.Field(CreatePaste)
