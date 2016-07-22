import django.conf.urls


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
