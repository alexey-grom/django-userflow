# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=30, verbose_name='display name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_removed', models.BooleanField(default=False, verbose_name='removed')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('real_name', models.CharField(max_length=255, verbose_name='Real name', blank=True)),
                ('birthday', models.DateField(default=None, null=True, verbose_name='Birthday', blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, verbose_name='Gender', choices=[(b'm', 'Male'), (b'f', 'Female')])),
                ('location', models.CharField(max_length=255, verbose_name='Location', blank=True)),
                ('about', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to=b'avatars', verbose_name='Photo', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
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
