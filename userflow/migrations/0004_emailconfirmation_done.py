# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0003_emailconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailconfirmation',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
