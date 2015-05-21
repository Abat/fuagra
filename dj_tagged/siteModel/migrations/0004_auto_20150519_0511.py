# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('siteModel', '0003_auto_20150519_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateTimeField(verbose_name='Date Created', default=datetime.datetime(2015, 5, 19, 5, 11, 6, 585070, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(verbose_name='Date Updated', default=datetime.datetime(2015, 5, 19, 5, 11, 6, 585374, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='owner',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
