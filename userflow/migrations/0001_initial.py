# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(db_index=True, max_length=64, verbose_name='Contact type', choices=[(b'phone', 'Phone'), (b'facebook', 'Facebook'), (b'site', 'Site'), (b'skype', 'Skype')])),
                ('value', models.CharField(max_length=255, verbose_name='Contact value')),
                ('user', models.ForeignKey(related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_done', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_done', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Is primary')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active')),
                ('is_public', models.BooleanField(default=False, verbose_name='Is public')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'email',
                'verbose_name_plural': 'emails',
            },
        ),
        migrations.AddField(
            model_name='passwordresetconfirmation',
            name='email',
            field=models.ForeignKey(to='userflow.UserEmail'),
        ),
        migrations.AddField(
            model_name='emailconfirmation',
            name='email',
            field=models.ForeignKey(related_name='confirmations', to='userflow.UserEmail'),
        ),
    ]
