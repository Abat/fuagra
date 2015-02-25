from django.conf.urls import patterns, include, url
from django.contrib import admin
from siteModel import views

urlpatterns = patterns('',
    #url(r'^$', include('siteModel.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls))
)
