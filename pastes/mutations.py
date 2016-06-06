import graphene

from graphene import relay, with_context

from .models import Paste
from .nodes import PasteNode


class CreatePaste(graphene.Mutation):
    class Input:
        name = graphene.String().NonNull
        content = graphene.String().NonNull

    ok = graphene.Boolean()
    paste = relay.NodeField(PasteNode)

    @classmethod
    @with_context
    def mutate(cls, instance, arguments, context, info):
        user = context.user
        arguments = dict(arguments)
        arguments['owner'] = user if not user.is_anonymous() else None

        paste = Paste.objects.create(**arguments)
        ok = True
        return CreatePaste(paste=paste, ok=ok)
