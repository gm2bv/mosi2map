from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name = 'index'),
    url(r'^confirm/$', views.confirm, name = 'confirm'),
    url(r'^regist/$', views.regist, name = 'regist'),
    url(r'^event/(?P<event_id>[a-zA-Z0-9%#$@]+)/$', views.event, name = 'event'),
)

