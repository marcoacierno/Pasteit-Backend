from django.test import TestCase

from django.contrib.auth import get_user_model


class TestProfileSignals(TestCase):
    def test_create_user_should_create_a_profile(self):
        user = get_user_model().objects.create_user('User', 'hello@hello.it', password='hello')

        assert user.profile is not None
