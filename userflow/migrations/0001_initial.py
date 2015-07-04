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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(choices=[('skype', 'Skype'), ('facebook', 'Facebook'), ('phone', 'Phone'), ('site', 'Site')], db_index=True, verbose_name='Contact type', max_length=64)),
                ('value', models.CharField(max_length=255, verbose_name='Contact value')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='contacts')),
            ],
            options={
                'verbose_name_plural': 'contacts',
                'verbose_name': 'contact',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_done', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordResetConfirmation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_done', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='email address')),
                ('is_primary', models.BooleanField(verbose_name='Is primary', default=False)),
                ('is_active', models.BooleanField(verbose_name='Is active', default=False)),
                ('is_public', models.BooleanField(verbose_name='Is public', default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='emails')),
            ],
            options={
                'verbose_name_plural': 'emails',
                'verbose_name': 'email',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='passwordresetconfirmation',
            name='email',
            field=models.ForeignKey(to='userflow.UserEmail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailconfirmation',
            name='email',
            field=models.ForeignKey(to='userflow.UserEmail', related_name='confirmations'),
            preserve_default=True,
        ),
    ]
