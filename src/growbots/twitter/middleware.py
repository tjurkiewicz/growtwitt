import django.shortcuts


class TwitterMiddleware(object):

    REDIRECT_VIEW = 'frontend:auth'

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Twitter authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        try:
            twitter_request_token = request.session['twitter_access_token']
            if twitter_request_token is None:
                return django.shortcuts.redirect(self.REDIRECT_VIEW)
        except KeyError:
            return django.shortcuts.redirect(self.REDIRECT_VIEW)
