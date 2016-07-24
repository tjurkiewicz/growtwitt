import django.views.generic

import growbots.views
import growbots.twitter.api
import growbots.twitter.views


class AuthView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass


class FollowersView(growbots.views.TemplateNameMixin,
                    growbots.twitter.views.TwitterOAuthMixin,
                    django.views.generic.TemplateView):

    def get_context_data(self, **kwargs):
        ctx = super(FollowersView, self).get_context_data(**kwargs)
        ctx['followers'] = growbots.twitter.api.get_followers(
            self.twitter_oauth_token, self.twitter_oauth_token_secret, self.twitter_user_id)

        return ctx
