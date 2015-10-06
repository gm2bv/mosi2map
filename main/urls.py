from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^regist/$', views.regist, name = 'regist'),
    url(r'^event/(?P<event_id>[\w%@]{20})/$', views.event, name = 'event'),
)

