from django.conf.urls import patterns, url
from siteModel import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)