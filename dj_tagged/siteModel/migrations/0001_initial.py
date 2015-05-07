# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('thumbs_up', models.IntegerField(default=0)),
                ('thumbs_down', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('content', models.CharField(max_length=2000)),
                ('child', models.ForeignKey(related_name='child_comment', to='siteModel.Comments')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2015, 5, 7, 4, 19, 19, 623850, tzinfo=utc), verbose_name=b'Date Created')),
                ('date_updated', models.DateTimeField(default=datetime.datetime(2015, 5, 7, 4, 19, 19, 623918, tzinfo=utc), verbose_name=b'Date Updated')),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('url', models.URLField(unique=True)),
                ('num_comments', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(upload_to=b'profile_pictures', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comments',
            name='news_id',
            field=models.ForeignKey(to='siteModel.News'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(related_name='parent_comment', to='siteModel.Comments'),
            preserve_default=True,
        ),
    ]
