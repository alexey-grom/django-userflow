# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userflow', '0004_auto_20150621_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=64, db_index=True)),
                ('value', models.CharField(max_length=255)),
                ('user', models.ForeignKey(related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
