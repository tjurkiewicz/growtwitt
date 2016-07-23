
import growbots.core.application

import growbots.frontend.config
import growbots.frontend.views


class FrontendApplication(growbots.core.application.Application):

    name = growbots.frontend.config.FrontendConfig.name
    app_name = 'frontend'

    views = [
        (growbots.frontend.views.AuthView, r'^$', 'auth',),
        (growbots.frontend.views.FollowersView, r'^followers/followers$', 'followers-of-followers',),
    ]


application = FrontendApplication()
