import factory

from factory import fuzzy

from fuzzy_utils import fuzzy_utils

from django.contrib.auth import get_user_model

from factory import django

from profiles.models import Profile


class ProfileFactory(django.DjangoModelFactory):
    class Meta:
        model = Profile


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fuzzy.FuzzyText()
    first_name = fuzzy.FuzzyText()
    last_name = fuzzy.FuzzyText()
    email = fuzzy_utils.FuzzyEmail()
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
