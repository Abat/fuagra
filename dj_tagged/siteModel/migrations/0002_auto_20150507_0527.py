# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('siteModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='owner',
            field=models.ForeignKey(default=1, to='siteModel.UserProfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 5, 26, 58, 188004, tzinfo=utc), verbose_name=b'Date Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 5, 26, 58, 188044, tzinfo=utc), verbose_name=b'Date Updated'),
            preserve_default=True,
        ),
    ]
