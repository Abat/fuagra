from django.forms import widgets
from rest_framework import serializers
from siteModel.models import News
from siteModel.models import User
from siteModel.models import Comments
from siteModel.models import Vote
from siteModel.models import NewsCategoryUserPermission

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
				return 'A'
			elif permission == 'MD':
				return 'M'
			elif permission == 'EX':
				return 'E'
		except NewsCategoryUserPermission.DoesNotExist:
			pass
		return "U"

	class Meta:
		model = News
		fields = ('id', 'title', 'date_created', 'date_updated', 'upvotes', 'downvotes', 'views', 'url', 'content', 'num_comments', 'owner', 'username', 'category', 'has_voted', 'submitter_role') 
		read_only_fields = ('id', 'date_created', 'date_updated', 'views', 'num_comments', 'owner', 'username', 'has_voted', 'submitter_role')
	
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class CommentSerializer(serializers.ModelSerializer):

	submitter_role = serializers.SerializerMethodField()
	is_submitter = serializers.SerializerMethodField()
	def get_submitter_role(self, obj):
		try:
			user_permission = NewsCategoryUserPermission.objects.get(user = obj.owner, category = obj.news.category)
			permission = user_permission.permission
			if permission == 'AD':
				return 'A'
			elif permission == 'MD':
				return 'M'
			elif permission == 'EX':
				return 'E'
		except NewsCategoryUserPermission.DoesNotExist:
			pass
		return "U"

	def get_is_submitter(self, obj):
		if obj.owner == obj.news.owner:
			return 1
		return 0
		
	class Meta:
		model = Comments
		read_only_fields = ('id', 'date_created', 'thumbs_up', 'thumbs_down', 'owner', 'username', 'submitter_role', 'is_submitter')

class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ('news', 'vote_status')
