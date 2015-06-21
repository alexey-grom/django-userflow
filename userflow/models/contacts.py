# encoding: utf-8

import re
from weakref import WeakValueDictionary

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
import six


__all__ = 'Contact', 'get_contact_types',


class ContactTypeMeta(type):
    register = WeakValueDictionary()

    def __new__(cls, name, bases, namespace):
        abstract = namespace.pop('abstract', False)

        Class = super(ContactTypeMeta, cls).__new__(cls, name, bases, namespace)
        if not abstract:
            assert Class.alias
            assert Class.title
            ContactTypeMeta.register[Class.alias] = Class

        return Class


class ContactType(six.with_metaclass(ContactTypeMeta)):
    abstract = True
    alias = None
    title = None

    def validate(self, value):
        pass


class RegexContactType(ContactType):
    abstract = True
    regex = None

    def validate(self, value):
        if self.regex and not re.match(self.regex, value):
            raise ValidationError('Invalid value')


class SiteContactType(ContactType):
    alias = 'site'
    title = _(u'Site')

    def validate(self, value):
        URLValidator()(value)


class SkypeContactType(RegexContactType):
    alias = 'skype'
    title = _('Skype')
    regex = re.compile(r'^[a-z][[a-z0-9.-]{5,31}$', re.IGNORECASE or re.UNICODE)


class FacebookContactType(RegexContactType):
    alias = 'facebook'
    title = _('Facebook')
    regex = re.compile(r'(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?',
                       re.IGNORECASE)


def get_contact_types():
    return ((item.alias, item.title)
            for item in ContactTypeMeta.register.itervalues())


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts')
    type = models.CharField(max_length=64, db_index=True, choices=get_contact_types(), blank=False)
    value = models.CharField(max_length=255, blank=False)

    @property
    def contact_type(self):
        return ContactTypeMeta.register.get(self.type, None)

    def clean(self):
        if self.type or self.value:
            Type = self.contact_type
            if Type is None:
                raise ValidationError(_('Unknown contact type'))
            print self.value, Type
            Type().validate(self.value)

    class Meta:
        app_label = 'userflow'
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
