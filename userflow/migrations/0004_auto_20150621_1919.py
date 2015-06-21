# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0003_auto_20150621_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='contact_phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contact_www',
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default=None, max_length=1, verbose_name='Gender', choices=[(b'm', 'Male'), (b'f', 'Female')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=255, verbose_name='Location', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(upload_to=b'avatars', verbose_name='Photo', blank=True),
        ),
    ]
