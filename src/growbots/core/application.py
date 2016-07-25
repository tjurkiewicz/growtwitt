import django.conf.urls
import django.core.urlresolvers


class Application(object):

    name = None
    app_name = None
    views = []

    def get_url(self, view_spec):
        view_class, pattern, name = view_spec
        return django.conf.urls.url(pattern, view_class.as_view(), name=name)

    def get_urls(self):
        return map(self.get_url, self.views)

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def reverse(self, view_name, *args, **kwargs):
        view_name = '{0}:{1}'.format(self.name, view_name)
        return django.core.urlresolvers.reverse(view_name, *args, **kwargs)
