import json
import uuid

import django.http.response
import django.views.generic

import growbots.views
import growbots.twitter.api
import growbots.twitter.models
import growbots.twitter.views


class AuthView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass


class FollowersView(growbots.views.TemplateNameMixin,
                    growbots.twitter.views.TwitterOAuthMixin,
                    django.views.generic.TemplateView):

    def get_followers(self):
        return growbots.twitter.api.get_followers(
            self.twitter_oauth_token, self.twitter_oauth_token_secret, self.twitter_screen_name)

    def get_context_data(self, **kwargs):
        ctx = super(FollowersView, self).get_context_data(**kwargs)
        ctx['followers'] = self.get_followers()
        ctx['uuid'] = uuid.uuid4().hex

        # Persist data inbetween
        growbots.twitter.models.FollowersCacheEntry.objects.bulk_create(
            growbots.twitter.models.FollowersCacheEntry(
                uuid4=ctx['uuid'],
                screen_name=screen_name,
                following=following
            ) for screen_name, following in ctx['followers'].iteritems()
        )

        return ctx


class FollowersAPIView(django.views.generic.View):
    """
        This might have been django's generic.ListView as well,
        but it's rather suitable for views rendered from a template.

        It's possible to incorporate ListView into json-api view, but
        in my opinion it's beyond this demo. This would require to change
        `response_class` to JSONResponse rather than template_response,
        and place object's to_json callback to something like `template_name`
        equivalent.
    """
    def format_follower(self, entry):
        return {
            'handle': '@{}'.format(entry['screen_name']),
            'order': entry['following'],
        }

    def get(self, request, *args, **kwargs):
        uuid4 = kwargs['uuid']

        cached = growbots.twitter.models.FollowersCacheEntry.objects.filter(uuid4=uuid4).\
            values('screen_name', 'following')

        if len(cached) > 0:
            content = json.dumps(list(map(self.format_follower, cached)))
            return django.http.response.HttpResponse(content, content_type='application/json')
        else:
            content = json.dumps({
                'error': 1,
                'message': 'No objects found.',
            })
            return django.http.response.HttpResponseNotFound(content, content_type='application/json')
