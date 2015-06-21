# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0005_contact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'contact', 'verbose_name_plural': 'contacts'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.CharField(db_index=True, max_length=64, choices=[(b'facebook', 'Facebook'), (b'site', 'Site'), (b'skype', 'Skype')]),
        ),
    ]
