# encoding: utf-8

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from userflow import conf


class UsersConfig(AppConfig):
    name = 'userflow'
    verbose_name = _('Users')
