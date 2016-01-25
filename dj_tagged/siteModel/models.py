from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation import SimpleEmailConfirmationUserMixin
from django.conf import settings

class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    pass

class NewsCategory(models.Model):
    title = models.CharField(max_length=100, primary_key=True)

class NewsCategoryUserPermission(models.Model):
    category = models.ForeignKey(NewsCategory)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    USER_TYPES = (
        ('AD', 'Admin'),
        ('MD', 'Moderator'),
        ('EX', 'Expert'),
        ('US', 'User') #We probably can just assume the user is by default a user.
    )
    permission = models.CharField(max_length=2, choices=USER_TYPES, default = 'US')
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('user', 'category'),)

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=400)
    date_created = models.DateTimeField('Date Created', default=timezone.now)
    date_updated = models.DateTimeField('Date Updated', default=timezone.now)
    # web url of a news
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    url = models.URLField(unique=True)
    num_comments = models.IntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    username = models.CharField(max_length=100)
    category = models.ForeignKey(NewsCategory, default = "Test")
    # class Meta:
    #     ordering = ['-date_updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/api/news/%i/" % self.id

    def get_creation_date(self):
        return self.date_created
        
    def get_ups(self):
        return self.upvotes

    def get_downs(self):
        return self.downvotes


class Comments(models.Model):
    news = models.ForeignKey(News)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True)
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    content = models.CharField(max_length=2000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    username = models.CharField(max_length=100)
    isExpert = models.BooleanField(default=False)
    date_created = models.DateTimeField('Date Created', default=timezone.now)

    #class Meta:
        #ordering = ['-date_created']

    def __str__(self):
        return self.content

    def get_creation_date(self):
        return self.date_created

    def get_ups(self):
        return self.thumbs_up

    def get_downs(self):
        return self.thumbs_down



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    avatar = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username

class Vote(models.Model):
    CLEAR_STATUS = 0
    DOWNVOTE_STATUS = -1
    UPVOTE_STATUS = 1
    VOTE_CHOICES = (
        (CLEAR_STATUS, 'Clear'),
        (DOWNVOTE_STATUS, 'Downvote'),
        (UPVOTE_STATUS, 'Upvote'),
    )
    news = models.ForeignKey(News)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    vote_status = models.SmallIntegerField(choices=VOTE_CHOICES, default=0)

    class Meta:
        unique_together = ('user', 'news',)
