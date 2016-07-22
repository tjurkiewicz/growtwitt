import pytest

import views

def test_template_name():
    class SomeView(views.TemplateView):
        pass

    view = SomeView()
    assert view.get_template_names() == ['growbots/some.html']