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
            field=models.CharField(db_index=True, max_length=64, choices=[('facebook', 'Facebook'), ('phone', 'Phone'), ('site', 'Site'), ('skype', 'Skype')], verbose_name='Contact type'),
        ),
        migrations.AlterField(
            model_name='useremail',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
