# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_id', models.IntegerField(default=-1)),
                ('partent_id', models.IntegerField(default=-1)),
                ('child_id', models.IntegerField(default=-1)),
                ('user_id', models.IntegerField(default=-1)),
                ('thumbs_up', models.IntegerField(default=0)),
                ('thumbs_down', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('content', models.CharField(max_length=2000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news_id', models.IntegerField(default=-1)),
                ('date_created', models.DateTimeField(verbose_name=b'Date Created')),
                ('source', models.CharField(max_length=200)),
                ('num_comments', models.IntegerField(default=0)),
                ('num_accesses', models.IntegerField(default=0)),
                ('contents_link', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
