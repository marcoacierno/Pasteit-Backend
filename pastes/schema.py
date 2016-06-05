import graphene

from graphene import relay, with_context

from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.filter.fields import DjangoFilterConnectionField

from .models import Paste


class PasteNode(DjangoNode):
    node = relay.NodeField()
    owner = graphene.Field('UserNode')
    visibility = graphene.String()
    is_my_paste = graphene.Boolean()

    @with_context
    def resolve_is_my_paste(self, args, context, info):
        user = context.user

        if user.is_anonymous():
            return False

        return self.owner == user

    class Meta:
        model = Paste
        filter_order_by = ('-modified', '-created', )


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
