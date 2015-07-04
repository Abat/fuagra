# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('siteModel', '0005_auto_20150703_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 4, 0, 24, 57, 983142, tzinfo=utc), verbose_name='Date Updated'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comments',
            name='child',
            field=models.ForeignKey(related_name='child_comment', default=-1, to='siteModel.Comments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(related_name='parent_comment', default=-1, to='siteModel.Comments'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 4, 0, 24, 57, 981214, tzinfo=utc), verbose_name='Date Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 4, 0, 24, 57, 981583, tzinfo=utc), verbose_name='Date Updated'),
            preserve_default=True,
        ),
    ]
