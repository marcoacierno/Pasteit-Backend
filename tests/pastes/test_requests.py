from django.test import TestCase

from tests.factories import PasteFactory

from api.schema import schema


class TestGraphQLPastesRequest(TestCase):
    def test_get_all_pastes(self):
        p1 = PasteFactory(visibility='public')
        p2 = PasteFactory(visibility='public')

        query = '''
            query {
                pastes {
                    edges {
                        node {
                            name
                            visibility
                            content
                        }
                    }
                }
            }
'''
        result = schema.execute(query)

        assert not result.errors
        assert {
            'node': {
                'name': p1.name,
                'visibility': p1.visibility,
                'content': p1.content,
            },
        } in result.data['pastes']['edges']

        assert {
            'node': {
                'name': p2.name,
                'visibility': p2.visibility,
                'content': p2.content,
            },
        } in result.data['pastes']['edges']

    def test_pastes_doesnt_expose_private_pastes(self):
        public = PasteFactory(visibility='public')
        private = PasteFactory(visibility='private')

        query = '''
            query {
                pastes {
                    edges {
                        node {
                            name
                            visibility
                        }
                    }
                }
            }
'''

        result = schema.execute(query)

        assert not result.errors
        assert len(result.data['pastes']['edges']) == 1
        assert {
            'node': {
                'name': public.name,
                'visibility': public.visibility,
            },
        } in result.data['pastes']['edges']

        assert {
            'node': {
                'name': private.name,
                'visibility': private.visibility,
            },
        } not in result.data['pastes']['edges']

    def test_pastes_doesnt_expose_unlisted_pastes(self):
        public = PasteFactory(visibility='public')
        unlisted = PasteFactory(visibility='unlisted')

        query = '''
            query {
                pastes {
                    edges {
                        node {
                            name
                            visibility
                        }
                    }
                }
            }
'''

        result = schema.execute(query)

        assert not result.errors
        assert len(result.data['pastes']['edges']) == 1
        assert {
            'node': {
                'name': public.name,
                'visibility': public.visibility,
            },
        } in result.data['pastes']['edges']

        assert {
            'node': {
                'name': unlisted.name,
                'visibility': unlisted.visibility,
            },
        } not in result.data['pastes']['edges']

    def test_get_paste_owner_info(self):
        paste = PasteFactory(visibility='public')

        query = '''
            query {
                pastes {
                    edges {
                        node {
                            name
                            owner {
                                user {
                                    username
                                }
                            }
                        }
                    }
                }
            }
'''

        result = schema.execute(query)
        assert not result.errors
        assert (
            result.data['pastes']['edges'][0]['node']['owner']['user']['username'] ==
            paste.owner.user.username
        )

    def test_pastes_are_ordered_by_modified(self):
        p1 = PasteFactory(visibility='public')
        p2 = PasteFactory(visibility='public')

        query = '''
            query {
                pastes {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }
'''

        result = schema.execute(query)
        assert not result.errors

        fs = sorted([p1, p2], key=sortByModified)
        fs.reverse()

        s = sorted(fs, key=sortByCreated)
        s.reverse()

        assert {
            'node': {
                'name': s[0].name,
            },
        } == result.data['pastes']['edges'][0]

        assert {
            'node': {
                'name': s[1].name,
            },
        } == result.data['pastes']['edges'][1]


def sortByCreated(obj):
    return obj.created


def sortByModified(obj):
    return obj.modified
