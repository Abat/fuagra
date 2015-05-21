from django.forms import widgets
from rest_framework import serializers
from siteModel.models import News
from siteModel.models import UserProfile


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'date_created', 'date_updated', 'likes', 'views', 'url', 'num_comments', 'owner') 
        read_only_fields = ('date_created', 'date_updated', 'likes', 'views', 'num_comments', 'owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username',) 
