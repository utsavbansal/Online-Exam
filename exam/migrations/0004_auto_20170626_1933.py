# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 14:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20170625_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='candidate',
            name='last_name',
            field=models.CharField(default=datetime.datetime(2017, 6, 26, 14, 2, 43, 785000, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='password',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='user_name',
            field=models.CharField(default=datetime.datetime(2017, 6, 26, 14, 3, 12, 224000, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]