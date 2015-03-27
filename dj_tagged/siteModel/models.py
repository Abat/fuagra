from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField('Date Created', default=datetime.now)
    date_updated = models.DateTimeField('Date Updated', default=datetime.now)
    # web url of a news
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    url = models.URLField()
    num_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comments(models.Model):
    news_id = models.ForeignKey(News)
    parent = models.ForeignKey('self', related_name='parent_comment')
    child = models.ForeignKey('self', related_name='child_comment')
    user_id = models.IntegerField()
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    content = models.CharField(max_length=2000)

    def __str__(self):
        return self.content

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    avatar = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username
