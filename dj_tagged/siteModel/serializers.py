from django.forms import widgets
from rest_framework import serializers
from siteModel.models import News
from siteModel.models import User
from siteModel.models import Comments
from siteModel.models import Vote
from siteModel.models import NewsCategoryUserPermission
from siteModel.models import CommentVote


class NewsSerializer(serializers.ModelSerializer):
	has_voted = serializers.SerializerMethodField()
	submitter_role = serializers.SerializerMethodField()
	def get_has_voted(self, obj):
		request = self.context.get('request', None)
		if request is not None and not request.user.is_anonymous():
			try:
				vote = Vote.objects.get(news = obj, user = request.user)
				return vote.vote_status;
			except Vote.DoesNotExist:
				pass;
		return 0;

	def get_submitter_role(self, obj):
		try:
			user_permission = NewsCategoryUserPermission.objects.get(user = obj.owner, category = obj.category)
			permission = user_permission.permission
			if permission == 'AD':
				return 'AD'
			elif permission == 'MD':
				return 'MD'
			elif permission == 'EX':
				return 'EX'
		except NewsCategoryUserPermission.DoesNotExist:
			pass
		return "US"

	class Meta:
		model = News
		fields = ('id', 'title', 'date_created', 'date_updated', 'upvotes', 'downvotes', 'views', 'url', 'content', 'num_comments', 'owner', 'username', 'category', 'has_voted', 'submitter_role', 'thumbnail_image') 
		read_only_fields = ('id', 'date_created', 'date_updated', 'views', 'num_comments', 'owner', 'username', 'has_voted', 'submitter_role', 'thumbnail_image')
	
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class CommentSerializer(serializers.ModelSerializer):

	submitter_role = serializers.SerializerMethodField()
	is_op = serializers.SerializerMethodField()
	def get_submitter_role(self, obj):
		try:
			user_permission = NewsCategoryUserPermission.objects.get(user = obj.owner, category = obj.news.category)
			permission = user_permission.permission
			if permission == 'AD':
				return 'AD'
			elif permission == 'MD':
				return 'MD'
			elif permission == 'EX':
				return 'EX'
		except NewsCategoryUserPermission.DoesNotExist:
			pass
		return "US"

	def get_is_op(self, obj):
		if obj.owner == obj.news.owner:
			return 1
		return 0
		
	class Meta:
		model = Comments
		read_only_fields = ('id', 'date_created', 'thumbs_up', 'thumbs_down', 'owner', 'username', 'submitter_role', 'is_op')

class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ('news', 'vote_status')

class CommentVoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentVote
		fields = ('comment', 'vote_status')
