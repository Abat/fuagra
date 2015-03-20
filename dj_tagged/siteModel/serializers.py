from django.forms import widgets
from rest_framework import serializers
from siteModel.models import News
from django.contrib.auth.models import User


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'date_created', 'date_updated', 'likes', 'views', 'url', 'num_comments') 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',) 
