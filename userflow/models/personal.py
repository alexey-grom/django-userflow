# encoding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = 'UserInfoMixin',


GENDERS = {'f': _(u'Female'),
           'm': _(u'Male')}


class UserInfoMixin(models.Model):
    real_name = models.CharField(max_length=255, blank=True, verbose_name=_('Real name'))
    birthday = models.DateField(default=None, null=True, blank=True, verbose_name=_('Birthday'))
    gender = models.CharField(max_length=1, choices=GENDERS.items(), blank=True, verbose_name=_('Gender'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    about = models.TextField(blank=True)
    photo = models.ImageField(upload_to='avatars', blank=True, verbose_name=_('Photo'))

    class Meta:
        abstract = True
