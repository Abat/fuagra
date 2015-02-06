from django.db import models

# Create your models here.
class News(models.Model):
    news_id = models.IntegerField(default=-1)
    date_created = models.DateTimeField('Date Created')
    # web url of a news
    source = models.CharField(max_length=200)
    num_comments = models.IntegerField(default=0)
    num_accesses = models.IntegerField(default=0)
    contents_link = models.CharField(max_length=200)

class Comments(models.Model):
    comment_id = models.IntegerField(default=-1)
    partent_id = models.IntegerField(default=-1)
    child_id = models.IntegerField(default=-1)
    user_id = models.IntegerField(default=-1)
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    content = models.CharField(max_length=2000) 