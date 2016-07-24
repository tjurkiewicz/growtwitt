import django.http
import django.shortcuts
import django.views.generic

import growbots.twitter.api
import growbots.views


class AuthView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass


class TwitterLogoutView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        for k in ('twitter_request_token', 'twitter_access_token'):
            if k in request.session:
                del request.session[k]
        return django.shortcuts.redirect('frontend:auth')


class TwitterRequestTokenView(django.views.generic.View):

    def post(self, request, *args, **kwargs):
        twitter_request_token = growbots.twitter.api.get_request_token(request)
        request.session['twitter_request_token'] = twitter_request_token
        print "Twitter request token", twitter_request_token

        redirect_url = growbots.twitter.api.get_user_redirect_url(twitter_request_token['oauth_token'])
        return django.http.HttpResponseRedirect(redirect_url)


class TwitterAcceptView(django.views.generic.View):

    def get(self, request, *args, **kwargs):
        try:
            if request.GET['oauth_token'] != request.session['twitter_request_token']['oauth_token']:
                return django.http.HttpResponseForbidden(content='Mismatched oauth_tokens')
            if not request.GET['oauth_verifier']:
                return django.http.HttpResponseForbidden(content='Mismatched oauth_verifier')
        except KeyError:
            # Don't be too generous. It's missing, either in session or in request query.
            return django.http.HttpResponseForbidden(content='Missing oauth_token')

        oauth_verifier = request.GET['oauth_verifier']
        oauth_token = request.GET['oauth_token']
        oauth_token_secret = request.session['twitter_request_token']['oauth_token_secret']
        twitter_access_token = growbots.twitter.api.get_access_token(oauth_token, oauth_token_secret, oauth_verifier)
        print "Twitter access token", twitter_access_token

        request.session['twitter_access_token'] = twitter_access_token
        del request.session['twitter_request_token']

        return django.shortcuts.redirect('frontend:followers-of-followers')


class TwitterOAuthMixin(object):
    oauth_keys = ('oauth_token', 'oauth_token_secret', 'user_id', 'screen_name')

    def dispatch(self, request, *args, **kwargs):
        for k in self.oauth_keys:
            try:
                key = 'twitter_{}'.format(k)
                value = self.request.session['twitter_access_token'][k]
                setattr(self, key, value)
            except KeyError:
                return django.shortcuts.redirect('frontend:auth')

        return super(TwitterOAuthMixin, self).dispatch(request, *args, **kwargs)

