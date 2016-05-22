import factory

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from profiles.signals import create_profile

from factory import fuzzy

from fuzzy_utils import fuzzy_utils

from factory import django

from profiles.models import Profile

from pastes.models import Paste


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fuzzy.FuzzyText()
    first_name = fuzzy.FuzzyText()
    last_name = fuzzy.FuzzyText()
    email = fuzzy_utils.FuzzyEmail()
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    profile = factory.RelatedFactory('tests.factories.ProfileFactory', 'user')

    @classmethod
    def _generate(cls, create, attrs):
        post_save.disconnect(create_profile, get_user_model())
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_profile, get_user_model())
        return user


class ProfileFactory(django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)


VISIBILITY_CHOICES = [x for x, _ in Paste.VISIBILITY]


class PasteFactory(django.DjangoModelFactory):
    class Meta:
        model = Paste

    name = fuzzy.FuzzyText()
    owner = factory.SubFactory(UserFactory)
    visibility = fuzzy.FuzzyChoice(choices=VISIBILITY_CHOICES)
    content = fuzzy.FuzzyText()
