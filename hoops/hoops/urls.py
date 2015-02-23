from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hoops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^games/', include('games.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', RedirectView.as_view(url=reverse_lazy("games.views.history")))
)
