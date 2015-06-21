# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0002_useremail_is_public'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(default=None, null=True, verbose_name='Birthday', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_phone',
            field=models.URLField(verbose_name='Phone', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_www',
            field=models.URLField(verbose_name='Website link', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='real_name',
            field=models.CharField(max_length=255, verbose_name='Real name', blank=True),
        ),
    ]
