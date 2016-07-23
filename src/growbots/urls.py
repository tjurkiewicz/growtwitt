import growbots.core.urls


urlpatterns = growbots.core.urls.get_patterns(
    (r'^',         'growbots.frontend.app'),
    (r'^twitter/', 'growbots.twitter.app')
)
