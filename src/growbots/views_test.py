import views


def test_template_name():
    class SomeView(views.TemplateNameMixin):
        pass

    view = SomeView()
    assert view.get_template_names() == ['growbots/some.html']
