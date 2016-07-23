import django.http
import django.shortcuts
import django.views.generic

import growbots.twitter.api
import growbots.views


class AuthView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass


class TwitterRequestTokenView(django.views.generic.View):

    def post(self, request, *args, **kwargs):
        twitter_request_token = growbots.twitter.api.get_request_token(request)
        request.session['twitter_request_token'] = twitter_request_token

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
        twitter_access_token = growbots.twitter.api.get_access_token(oauth_verifier)

        request.session['twitter_access_token'] = twitter_access_token
        del request.session['twitter_request_token']

        return django.shortcuts.redirect('frontend:followers-of-followers')
