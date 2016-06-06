from django.test import TestCase, Client

from tests.factories import UserFactory, PasteFactory

from tests.utils import create_url


class TestGraphQLUsersQuery(TestCase):
    def setUp(self):
        self.user = UserFactory(password='hello')

        self.client = Client()
        self.client.login(username=self.user.username, password='hello')

    def test_get_current_logged_user_username(self):
        query = '''
            query {
                me {
                    username
                }
            }
'''
        response = self.client.get(create_url(query))

        assert response.status_code == 200

        data = response.json()

        assert 'errors' not in data

        result = data['data']

        assert result['me']['username'] == self.user.username

    def test_cannot_use_me_query_if_not_logged(self):
        self.client.logout()

        query = '''
            query {
                me {
                    username
                }
            }
'''

        response = self.client.get(create_url(query))

        # TODO: We should return 400
        assert response.status_code == 200

        data = response.json()

        assert data['me'] is None

        # assert 'errors' in data
        # assert data['errors'][0]['message'] == 'You cannot query yourself if you are not logged'

    def test_get_user_pastes(self):
        paste = PasteFactory(owner=self.user)

        query = '''
            query {
                me {
                    pastes {
                        edges {
                            node {
                                name
                            }
                        }
                    }
                }
            }
'''

        response = self.client.get(create_url(query))

        assert response.status_code == 200

        data = response.json()

        assert len(data['data']['me']['pastes']['edges']) == 1

        first_paste = data['data']['me']['pastes']['edges'][0]['node']

        assert first_paste['name'] == paste.name
