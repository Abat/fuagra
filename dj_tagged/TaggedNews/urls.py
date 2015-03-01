from django.conf.urls import patterns, include, url
from django.contrib import admin
from siteModel import views

urlpatterns = patterns('',
    #url(r'^$', include('siteModel.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    # api starts here
    url(r'^api/news/$', views.news_list),
    url(r'^api/news/(?P<pk>[0-9]+)/$', views.news_detail),
)
