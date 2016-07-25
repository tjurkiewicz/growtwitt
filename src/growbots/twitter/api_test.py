
import api
import json


class MockClient(object):
    responses = {
        'prince':  ('bob', 'rick'),
        'bob': ('andrew',),
        'rick': ('andrew',),
    }

    def __init__(self, *args, **kwargs):
        pass

    def request(self, url, method='GET'):
        response = {'status': '200'}

        # Easy on this, don't use a key which accidentaly get matched (eg. `user`)
        for k in self.responses:
            if k in url:
                followers = ({'screen_name': f } for f in self.responses[k])
                return response, json.dumps({'users': list(followers), 'next_cursor': 0})

        # Test data set is not closed.
        raise NotImplementedError


def test_get_followers(monkeypatch):
    monkeypatch.setattr('oauth2.Client', MockClient)

    followers = api.get_followers('oauth_token', 'oauth_token_secret', 'prince')
    assert followers == {'andrew': 2}