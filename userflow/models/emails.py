# encoding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from userflow import conf


__all__ = 'UserEmail',


class UserEmailQueryset(models.QuerySet):
    def inactive(self):
        return self.filter(is_active=False)

    def active(self):
        return self.filter(is_active=True)

    def public(self):
        return self.filter(is_public=True)


class UserEmail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails')
    email = models.EmailField(_('email address'), unique=True, blank=False)

    is_primary = models.BooleanField(default=False, verbose_name=_('Is primary'))
    is_active = models.BooleanField(default=False, verbose_name=_('Is active'))
    is_public = models.BooleanField(default=False, verbose_name=_('Is public'))

    created = models.DateTimeField(auto_now_add=True)

    objects = UserEmailQueryset.as_manager()

    def __unicode__(self):
        return self.email
    __str__ = __unicode__

    @property
    def is_dummy(self):
        return self.email == conf.USERS_DUMMY_EMAIL

    class Meta:
        app_label = 'userflow'
        verbose_name = _('email')
        verbose_name_plural = _('emails')
