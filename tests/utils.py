from django.core.urlresolvers import reverse


ENDPOINT = reverse('graphql')


def create_url(query):
    return ENDPOINT + '?query=' + query
