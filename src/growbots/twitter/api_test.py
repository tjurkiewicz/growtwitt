
import api
import json
import urlparse


class MockClient(object):
    responses = {
        ('prince', -1):  (('bob', 'rick'), 1),
        ('prince', 1):   (('jeff', 'ed'),  0),
        ('bob', -1):     (('andrew',),     0),
        ('rick', -1):    (('andrew',),     0),
        ('jeff', -1):    (('marie',),      0),
        ('ed',   -1):    (('marie',),      0),
    }

    def __init__(self, *args, **kwargs):
        pass

    def request(self, url, method='GET'):
        response = {'status': '200'}

        parsed_url = urlparse.urlparse(url)
        qsl = dict(urlparse.parse_qsl(parsed_url.query))
        screen_name, cursor = qsl['screen_name'], int(qsl['cursor'])

        followers, next_cursor = self.responses[(screen_name, cursor)]

        return response, json.dumps({
            'next_cursor': next_cursor,
            'users': [{'screen_name': f} for f in followers],
        })


def test_get_followers(monkeypatch):
    monkeypatch.setattr('oauth2.Client', MockClient)

    followers = api.get_followers('oauth_token', 'oauth_token_secret', 'prince')
    assert followers == {'andrew': 2, 'marie': 2, }
