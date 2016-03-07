from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation import SimpleEmailConfirmationUserMixin
from django.conf import settings
import urllib
from urlparse import urlparse
import os
import logging
from siteModel.opengraph.opengraph import *
from django.core.files import File
from PIL import Image
import uuid
import cStringIO
import imghdr

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
        ('US', 'User'), #We probably can just assume the user is by default a user.
        ('BN', 'Banned')
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
    url = models.URLField(null=True, blank=True)
    content = models.CharField(max_length=2000, null=True, blank=True)
    num_comments = models.IntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    username = models.CharField(max_length=100)
    category = models.ForeignKey(NewsCategory, default = "Test")
    thumbnail_image = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    number_of_tries = models.IntegerField(default=0)
    #thumbnail_url = models.URLField(unique=True, null=True, blank=True)
    ##TODO
    #thumbnail_image = models.ImageField(upload_to='news_images', null=True, blank=True)
    class Meta:
        unique_together = (('owner', 'url'),)

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

    def save(self, *args, **kwargs):
        

        logger = logging.getLogger("django")
        thumbnail_url = None;
        if self.url and not self.thumbnail_image and self.number_of_tries < 1 and not self.category.title == "News" \
                                                                              and not self.category.title == "Sayasat" \
                                                                              and not self.category.title == "Raznoe":
            try:
                self.number_of_tries += 1
                og = IMPORTMEPLZ(self.url)
                if og.is_valid():
                    image_link = og.image
                    if (image_link):
                        thumbnail_url = str(image_link)
                        #TODO image.
            except:
                logger.info("Failed to dl image, either doesnt exist or error.")
        if thumbnail_url:
            
            file_save_dir = 'siteModel/static/thumbnails'

            response = urllib.urlopen(thumbnail_url)
            data = response.read()
            text_data = cStringIO.StringIO(data)
            image_type = imghdr.what(text_data)
            filename = self.category.title + '-' + str (uuid.uuid4()) + '.' + str(image_type)

            saved_img = open(os.path.join(file_save_dir, filename), 'wb')
            saved_img.write(data)
            saved_img.close()
            
            im = Image.open(os.path.join(file_save_dir, filename))

            basewidth = 70
            wpercent = (basewidth/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im_resize = im.resize((basewidth,hsize), Image.ANTIALIAS)

            im_resize.save(os.path.join(file_save_dir, filename))
            self.thumbnail_image = os.path.join(filename)
        super(News, self).save(*args, **kwargs) # Call the "real" save() method.


class Comments(models.Model):
    news = models.ForeignKey(News)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
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
        return self.upvotes

    def get_downs(self):
        return self.downvotes



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

class CommentVote(models.Model):
    CLEAR_STATUS = 0
    DOWNVOTE_STATUS = -1
    UPVOTE_STATUS = 1
    VOTE_CHOICES = (
        (CLEAR_STATUS, 'Clear'),
        (DOWNVOTE_STATUS, 'Downvote'),
        (UPVOTE_STATUS, 'Upvote'),
    )
    comment = models.ForeignKey(Comments)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    vote_status = models.SmallIntegerField(choices=VOTE_CHOICES, default=0)

    class Meta:
        unique_together = ('user', 'comment',)

# Create your models here.
class PasswordResetRequest(models.Model):
    
    date_valid = models.DateTimeField('Valid until', default=timezone.now)
    email = models.EmailField(primary_key=True)
    request_id = models.CharField(max_length=64,unique=True)
    
    def is_expired(self):
        if timezone.now() >= self.date_valid:
            return True
        return False
    
    @staticmethod
    def expire_time_delta():
        return timedelta(hours = 1)
