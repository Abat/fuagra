# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('siteModel', '0002_auto_20150507_0527'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='owner',
            field=models.ForeignKey(default=1, to='siteModel.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 5, 2, 37, 605080, tzinfo=utc), verbose_name='Date Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 19, 5, 2, 37, 605368, tzinfo=utc), verbose_name='Date Updated'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='owner',
            field=models.ForeignKey(default=1, to='siteModel.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to='profile_pictures', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
