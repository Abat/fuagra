from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=400)
    date_created = models.DateTimeField('Date Created', default=timezone.now())
    date_updated = models.DateTimeField('Date Updated', default=timezone.now())
    # web url of a news
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    url = models.URLField(unique=True)
    num_comments = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', default=1)	

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/api/news/%i/" % self.id

class Comments(models.Model):
    news = models.ForeignKey(News)
    parent = models.ForeignKey('self', related_name='parent_comment', default=-1)
    child = models.ForeignKey('self', related_name='child_comment', default=-1)
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    content = models.CharField(max_length=2000)
    owner = models.ForeignKey('auth.User')
    isExpert = models.BooleanField(default=False)
    date_created = models.DateTimeField('Date Updated', default=timezone.now())

    def __str__(self):
        return self.content

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    avatar = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username
