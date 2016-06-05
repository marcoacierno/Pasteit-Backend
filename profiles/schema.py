import graphene

from django.contrib.auth import get_user_model

from graphene import relay, with_context

from graphene.contrib.django import DjangoNode


class UserNode(DjangoNode):
    pastes = relay.ConnectionField('PasteNode')
    node = relay.NodeField()

    def resolve_pastes(self, args, info):
        return self.pastes.all()

    class Meta:
        model = get_user_model()
        exclude_fields = ('is_staff', 'is_superuser', 'password', 'is_active', 'user')


class Query(graphene.ObjectType):
    node = relay.NodeField()
    me = graphene.Field(UserNode)

    @with_context
    def resolve_me(self, args, context, info):
        me = context.user

        if me.is_anonymous() is True:
            return None
            # raise ValueError('You cannot query yourself if you are not logged')

        return me

    class Meta:
        abstract = True
