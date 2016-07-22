
import growbots.core.application

import growbots.frontend.config
import growbots.frontend.views


class FrontendApplication(growbots.core.application.Application):

    name = growbots.frontend.config.FrontendConfig.name
    app_name = 'abc'

    views = [
       (growbots.frontend.views.AuthView,  r'^$', 'auth',),
    ]


application = FrontendApplication()
