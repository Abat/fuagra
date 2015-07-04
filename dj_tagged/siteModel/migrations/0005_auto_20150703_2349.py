# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('siteModel', '0004_auto_20150519_0511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-date_updated']},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='news_id',
            new_name='news',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='isExpert',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date Created', default=datetime.datetime(2015, 7, 3, 23, 49, 2, 986592, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(verbose_name='Date Updated', default=datetime.datetime(2015, 7, 3, 23, 49, 2, 986888, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
