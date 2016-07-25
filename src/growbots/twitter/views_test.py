import httplib

import django.core.handlers.wsgi
import pytest

import app


@pytest.mark.django_db
def test_logout(client):
    response = client.get(app.application.reverse('logout'))
    assert response.status_code == httplib.FOUND
    assert response.url == '/'
    assert 'twitter_request_token' not in client.session
    assert 'twitter_access_token' not in client.session


@pytest.mark.django_db
def test_request_token_view(client, monkeypatch):
    def get_request_token(_):
        return {'oauth_token': 'whatever'}
    monkeypatch.setattr('growbots.twitter.api.get_request_token', get_request_token)

    response = client.post(app.application.reverse('request-token'))
    assert response.status_code == httplib.FOUND
    assert response.url == 'https://api.twitter.com/oauth/authenticate?oauth_token=whatever'
    assert 'twitter_request_token' in client.session
