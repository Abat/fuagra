from django.conf.urls import patterns, include, url
from django.contrib import admin
import notifications
from siteModel import views
from siteModel.views import NewsViewSet
from siteModel.views import UserViewSet
from siteModel.views import CommentViewSet
from siteModel.views import VoteViewSet

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

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
comment_detail = CommentViewSet.as_view({
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

vote_detail = VoteViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy',
})

vote_list = VoteViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

vote_upvote = VoteViewSet.as_view({
    'post': 'upvote',
})

vote_downvote = VoteViewSet.as_view({
    'post': 'downvote',
})
# vote_detail = VoteViewSet.as_view({
#     'get': 'retrieve',
# })

# vote_list = VoteViewSet.as_view({
#     'post': 'create'
# })

urlpatterns = patterns('',
    url(r'^about/?$', views.about, name='about'),
    url(r'^faq/?$', views.faq, name='faq'),
    #url(r'^submit/?$', views.submit, name='submit'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^login/?$', views.user_login, name='login'),
    url(r'^logout/?$', views.user_logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    # api starts here
    url(r'^api/news/?$', news_list, name='news-list'),
    url(r'^api/news/(?P<pk>[0-9]+)/?$', news_detail, name='news-detail'),
    url(r'^api/users/?$', user_list, name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/?$', user_detail, name='user-detail'),
    url(r'^api/users/(?P<category>\w+)/?$', views.check_user_permission, name='check_user_permission'),
    url(r'^api/comments/(?P<pk>[0-9]+)/(?P<comment_pk>[0-9]+)/?$', comment_detail, name='comment-detail'),
    url(r'^api/comments/(?P<pk>[0-9]+)/?$', comment_list, name='comment-list'),
    url(r'^api/permissions/', views.set_user_permission, name='set_user_permission'),
    url(r'^api/news/vote/(?P<news_id>[0-9]+)/?$', vote_list, name='vote-list'),
    url(r'^api/news/(?P<news_id>[0-9]+)/upvote/?$', vote_upvote, name='upvote'),
    url(r'^api/news/(?P<news_id>[0-9]+)/downvote/?$', vote_downvote, name='downvote'),
    url(r'^api/categories/?$', views.list_category, name='list_category'),

    url(r'^docs/', include('rest_framework_swagger.urls')),

    #Auth stuff
    # url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'siteModel/testOauth.html'}),
    # url(r'^api/hello', views.ApiEndpoint.as_view()),  # and also a resource server!
    # url(r'^secret$', views.secret_page, name='secret'),
    url(r'^accounts/confirmation/?$', views.confirm_email, name='confirm_email'),
    url(r'^accounts/resend_confirmation/$', views.resend_confirmation_email, name='resend_confirmation_email'),
    url(r'^notifications/$', views.notifications, name='fuagra_notifications'),
    url(r'^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    # catch all
    url(r'^.*$', views.index, name='index'),
)
