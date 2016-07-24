
import growbots.core.application

import growbots.twitter.config
import growbots.twitter.views


class TwitterApplication(growbots.core.application.Application):

    name = growbots.twitter.config.TwitterConfig.name
    app_name = 'twitter'

    views = [
        (growbots.twitter.views.TwitterRequestTokenView, r'^request_token$', 'request-token'),
        (growbots.twitter.views.TwitterAcceptView,       r'^accept_token$', 'accept-token'),
        (growbots.twitter.views.TwitterLogoutView,       r'^logout', 'logout'),
    ]


application = TwitterApplication()
