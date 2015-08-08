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
    icon = None

    def validate(self, value):
        pass

    def as_link(self, value):
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
    icon = 'world'

    def validate(self, value):
        URLValidator()(value)

    def as_link(self, value):
        return value


class SkypeContactType(RegexContactType):
    alias = 'skype'
    title = _('Skype')
    icon = 'skype'
    regex = re.compile(r'^[a-z][[a-z0-9.-]{5,31}$', re.IGNORECASE or re.UNICODE)

    def as_link(self, value):
        return 'skype:{}'.format(value)


class PhoneContactType(RegexContactType):
    alias = 'phone'
    title = _('Phone')
    icon = 'text telephone'
    regex = re.compile(r'^\+?[\d\-]{5,15}$', re.IGNORECASE or re.UNICODE)


class FacebookContactType(RegexContactType):
    alias = 'facebook'
    title = _('Facebook')
    icon = 'facebook'
    regex = re.compile(r'(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?',
                       re.IGNORECASE)

    def as_link(self, value):
        return value


def get_contact_types():
    items = ((item.alias, item.title)
             for item in ContactTypeMeta.register.values())
    items = sorted(items, key=lambda item: item[0])
    return items


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts')
    type = models.CharField(max_length=64, db_index=True, choices=get_contact_types(), blank=False, verbose_name=_('Contact type'))
    value = models.CharField(max_length=255, blank=False, verbose_name=_(u'Contact value'))

    @property
    def contact_type(self):
        return ContactTypeMeta.register.get(self.type, None)

    @property
    def contact_name(self):
        contact_type = self.contact_type
        if not contact_type:
            return
        return contact_type.title

    @property
    def as_link(self):
        contact_type = self.contact_type
        if not contact_type:
            return
        return contact_type().as_link(self.value)

    def clean(self):
        if self.type or self.value:
            Type = self.contact_type
            if Type is None:
                raise ValidationError(_('Unknown contact type'))
            Type().validate(self.value)

    class Meta:
        app_label = 'userflow'
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
