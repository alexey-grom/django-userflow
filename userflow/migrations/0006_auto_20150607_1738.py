# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0005_auto_20150607_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='email',
            field=models.ForeignKey(related_name='confirmations', to='userflow.UserEmail'),
        ),
    ]
