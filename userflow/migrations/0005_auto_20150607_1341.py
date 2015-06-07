# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0004_emailconfirmation_done'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailconfirmation',
            old_name='done',
            new_name='is_done',
        ),
    ]
