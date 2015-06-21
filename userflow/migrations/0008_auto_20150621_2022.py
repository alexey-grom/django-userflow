# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0007_auto_20150621_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=1, verbose_name='Gender', choices=[(b'm', 'Male'), (b'f', 'Female')]),
        ),
    ]
