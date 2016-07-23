import django.views.generic

import growbots.views


class AuthView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass


class FollowersView(growbots.views.TemplateNameMixin, django.views.generic.TemplateView):
    pass