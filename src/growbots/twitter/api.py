import httplib
import json
import os
import urllib
import urlparse

import django.core.urlresolvers
import oauth2


request_token_url = 'https://api.twitter.com/oauth/request_token'
auth_url = 'https://api.twitter.com/oauth/authenticate'
access_token_url = 'https://api.twitter.com/oauth/access_token'

followers_url = 'https://api.twitter.com/1.1/followers/list.json'
verify_credentials_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

class TwitterException(Exception):
    pass


class ConfigException(TwitterException):
    pass


class RuntimeException(TwitterException):
    pass


def get_value(key):
    try:
        return os.environ[key]
    except KeyError:
        raise ConfigException('{} not set in runtime environment.'.format(key))


def get_api_key():
    return get_value('TWITTER_API_KEY')


def get_api_secret():
    return get_value('TWITTER_API_SECRET')


def check_response(response):
    status = response['status']

    if status != str(httplib.OK):
        raise RuntimeException('Twitter backend responded with error code {}'.format(status))


def get_request_token(request):
    consumer = oauth2.Consumer(get_api_key(), get_api_secret())
    client = oauth2.Client(consumer)

    callback = request.build_absolute_uri(
        django.core.urlresolvers.reverse('twitter:accept-token'))
    params = urllib.urlencode({'oauth_callback': callback})

    response, content = client.request(request_token_url, method='POST', body=params)
    check_response(response)

    return dict(urlparse.parse_qsl(content))


def get_access_token(oauth_token, oauth_token_secret, oauth_verifier):
    consumer = oauth2.Consumer(get_api_key(), get_api_secret())
    token = oauth2.Token(oauth_token, oauth_token_secret)
    client = oauth2.Client(consumer, token=token)

    params = urllib.urlencode({'oauth_verifier': oauth_verifier})

    response, content = client.request(access_token_url, method='POST', body=params)
    check_response(response)

    return dict(urlparse.parse_qsl(content))


def get_user_redirect_url(oauth_token):
    return '{}?{}'.format(
        auth_url, urllib.urlencode({'oauth_token': oauth_token})
    )


def get_followers(oauth_token, oauth_token_secret, user_id, depth=2):
    consumer = oauth2.Consumer(get_api_key(), get_api_secret())
    token = oauth2.Token(oauth_token, oauth_token_secret)
    client = oauth2.Client(consumer, token=token)

    queue = set()

    response, content = client.request(verify_credentials_url)
    check_response(response)
    parsed_content = json.loads(content)
    queue.add(parsed_content['id'])

    print queue