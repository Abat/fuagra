from django.conf.urls import patterns, include, url
from django.contrib import admin
import notifications
from siteModel import views
from siteModel.views import NewsViewSet
from siteModel.views import UserViewSet
from siteModel.views import CommentViewSet
from siteModel.views import VoteViewSet
from siteModel.views import CommentVoteViewSet

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
    'post': 'create',
})

all_comment_list = CommentViewSet.as_view({
    'get': 'list_all',
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

comment_upvote = CommentVoteViewSet.as_view({
    'post': 'upvote',
})

comment_downvote = CommentVoteViewSet.as_view({
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
    url(r'^api/users/(?P<username>\w+)/?$', user_detail, name='user-detail'),
    url(r'^api/users/permissions/(?P<category>\w+)/?$', views.check_user_permission, name='check_user_permission'),
    url(r'^api/comments/?$', all_comment_list, name='all-comment-list'),
    url(r'^api/comments/(?P<pk>[0-9]+)/(?P<comment_pk>[0-9]+)/?$', comment_detail, name='comment-detail'),
    url(r'^api/comments/(?P<pk>[0-9]+)/?$', comment_list, name='comment-list'),
    url(r'^api/permissions/', views.set_user_permission, name='set_user_permission'),
    url(r'^api/news/vote/(?P<news_id>[0-9]+)/?$', vote_list, name='vote-list'),
    url(r'^api/news/(?P<news_id>[0-9]+)/upvote/?$', vote_upvote, name='vote_upvote'),
    url(r'^api/news/(?P<news_id>[0-9]+)/downvote/?$', vote_downvote, name='vote_downvote'),
    url(r'^api/comments/(?P<comment_id>[0-9]+)/upvote/?$', comment_upvote, name='comment_upvote'),
    url(r'^api/comments/(?P<comment_id>[0-9]+)/downvote/?$', comment_downvote, name='comment_downvote'),
    url(r'^api/categories/?$', views.list_category, name='list_category'),

    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^accounts/request_password_reset/?$', views.request_password_reset, name='request_password_reset'),
    url(r'^accounts/reset_password/?$', views.submit_password_change, name='submit_password_change'),
    url(r'^accounts/confirmation/?$', views.confirm_email, name='confirm_email'),
    url(r'^accounts/resend_confirmation/$', views.resend_confirmation_email, name='resend_confirmation_email'),
    url(r'^notifications/$', views.notifications, name='fuagra_notifications'),
    url(r'^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^locale/(?P<locale>\w+)/?$', views.locale),
    url(r'^api/news/suggest_title/?$', views.suggest_title),
    # catch all
    url(r'^.*$', views.index, name='index'),
)
