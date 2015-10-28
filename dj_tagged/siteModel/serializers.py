from django.forms import widgets
from rest_framework import serializers
from siteModel.models import News
from siteModel.models import UserProfile
from siteModel.models import Comments
from siteModel.models import Vote

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'date_created', 'date_updated', 'upvotes', 'downvotes', 'views', 'url', 'num_comments', 'owner') 
        read_only_fields = ('id', 'date_created', 'date_updated', 'views', 'num_comments', 'owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comments
		read_only_fields = ('id', 'date_created', 'thumbs_up', 'thumbs_down', 'owner')

class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ('news', 'upvoted', 'downvoted')
