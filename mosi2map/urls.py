from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mosi2map.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^main/', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
