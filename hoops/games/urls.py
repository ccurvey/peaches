from django.conf.urls import patterns, url

urlpatterns = patterns('games.views',
    url('^preview/', 'preview'),
    url('^history/', 'history'),
)
