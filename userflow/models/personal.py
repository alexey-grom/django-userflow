from collections import OrderedDict

from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = 'UserInfoMixin',


GENDER_MALE, GENDER_FEMALE = 'm', 'f',
GENDERS = OrderedDict((
    (GENDER_MALE, _(u'Male')),
    (GENDER_FEMALE, _(u'Female')),
))


class UserInfoMixin(models.Model):
    real_name = models.CharField(max_length=255, blank=True, verbose_name=_('Real name'))
    birthday = models.DateField(default=None, null=True, blank=True, verbose_name=_('Birthday'))
    gender = models.CharField(max_length=1, choices=GENDERS.items(), blank=True, verbose_name=_('Gender'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    about = models.TextField(blank=True, verbose_name=_('About'))
    photo = models.ImageField(upload_to='avatars', blank=True, verbose_name=_('Photo'))

    class Meta:
        abstract = True
