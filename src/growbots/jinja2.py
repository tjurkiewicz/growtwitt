from __future__ import absolute_import  # Python 2 only

import jinja2
import django.core.urlresolvers


def environment(**options):
    env = jinja2.Environment(**options)
    env.globals.update({
       'url': django.core.urlresolvers.reverse,
    })
    return env
