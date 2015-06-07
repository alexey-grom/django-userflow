# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useremail',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='useremail',
            old_name='primary',
            new_name='is_primary',
        ),
        migrations.AlterUniqueTogether(
            name='useremail',
            unique_together=set([('user', 'is_primary')]),
        ),
    ]
