import graphene

from graphene import relay, with_context

from graphene.contrib.django.types import DjangoNode

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
