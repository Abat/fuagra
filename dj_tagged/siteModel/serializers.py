from django.forms import widgets
from rest_framework import serializers
from siteModel.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('news_id', 'date_created', 'date_updated', 'source', 'num_comments', 'num_accesses', 'contents_link') 
