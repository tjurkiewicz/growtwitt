import json

import django.http.response
import django.views.generic


import growbots.views
import growbots.twitter.api
import growbots.twitter.views


class AuthView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass


class FollowersMixin(growbots.twitter.views.TwitterOAuthMixin):

    def get_followers(self):
        return growbots.twitter.api.get_followers(
            self.twitter_oauth_token, self.twitter_oauth_token_secret, self.twitter_screen_name)


class FollowersView(growbots.views.TemplateNameMixin,
                    FollowersMixin,
                    django.views.generic.TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(FollowersView, self).get_context_data(**kwargs)
        ctx['followers'] = self.get_followers()
        return ctx


class FollowersAPIView(growbots.views.TemplateNameMixin,
                    FollowersMixin,
                    django.views.generic.View):

    def format_follower(self, entry):
        screen_name, order = entry
        return {
            'handle': '@{}'.format(screen_name),
            'order': order,
        }

    def get(self, request, *args, **kwargs):
        followers = self.get_followers()
        content = json.dumps(list(map(self.format_follower, followers)))
        return django.http.response.HttpResponse(content, content_type='application/json')
