from django.conf.urls import patterns, url

urlpatterns = patterns('games.views',
    url('^preview/', 'preview'),
    url('^history/', 'history'),
    url('^add_game/', 'add_game'),
)
