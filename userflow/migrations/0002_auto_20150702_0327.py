# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.CharField(max_length=64, choices=[('site', 'Site'), ('phone', 'Phone'), ('facebook', 'Facebook'), ('skype', 'Skype')], db_index=True, verbose_name='Contact type'),
            preserve_default=True,
        ),
    ]
