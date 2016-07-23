import importlib

import django.conf.urls


def to_url(url_entry):
    regex, app_module_name = url_entry
    app = importlib.import_module(app_module_name)

    return django.conf.urls.url(
        regex,
        django.conf.urls.include(app.application.urls)
    )


def get_patterns(*url_entries):
    return map(to_url, url_entries)
