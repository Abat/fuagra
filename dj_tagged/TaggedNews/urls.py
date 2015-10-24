from django.conf.urls import patterns, include, url
from django.contrib import admin
from siteModel import views
from siteModel.views import NewsViewSet
from siteModel.views import UserViewSet
from siteModel.views import CommentList

news_list = NewsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
news_detail = NewsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    # url(r'^comments/(?P<pk>[0-9]+)/$', views.comments, name='comments'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    # api starts here
    url(r'^api/news/$', news_list, name='news-list'),
    url(r'^api/news/(?P<pk>[0-9]+)/$', news_detail, name='news-detail'),
    url(r'^api/users/$', user_list, name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^api/comments/(?P<pk>[0-9]+)/$', views.CommentList.as_view(), name='comments-list'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
	url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'siteModel/testOauth.html'}),
)
