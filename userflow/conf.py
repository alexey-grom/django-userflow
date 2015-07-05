# encoding: utf-8

import sys
import datetime
import importlib

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.http.response import HttpResponse

from userflow import utils


__all__ = ()


class setting(object):
    def __init__(self, name, default, auto_import=False):
        self.name = name
        self.default = default
        self.auto_import = auto_import

    def value(self):
        result = getattr(django_settings, self.name, self.default)
        if self.default:
            if type(result) != type(self.default):
                raise ImproperlyConfigured()
        if self.auto_import:
            if isinstance(result, (list, tuple)):
                result = map(import_attr, result)
            else:
                result = import_attr(result)
        return result


class settings(dict):
    def __init__(self, *args, **kwargs):
        iterable = ((item.name, item) for item in args)
        super(settings, self).__init__(iterable, **kwargs)

    def _check_value(self, item):
        assert isinstance(item, setting)
        return item.name, item.value()

    def update(self, other=None, **kwargs):
        raise RuntimeError

    def __getitem__(self, key):
        value = super(settings, self).__getitem__(key)
        if isinstance(value, setting):
            value = self[key] = value.value()
        return value


def import_attr(attr):
    module_name, attr = attr.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr, None)


SETTINGS = settings(
    setting('USERS_FLOW_UP',
            (
                'userflow.pipeline.auth.signup',
                'userflow.pipeline.mails.signup_email',
                'userflow.pipeline.activation.send_email_confirm',
                'userflow.pipeline.auth.signin',
                'userflow.pipeline.redirects.next_redirect',
                'userflow.pipeline.redirects.login_redirect',
            ),
            auto_import=True),

    setting('USERS_FLOW_DOWN',
            ('userflow.pipeline.auth.signout',
             'userflow.pipeline.redirects.next_redirect',
             'userflow.pipeline.redirects.index_redirect', ),
            auto_import=True),

    setting('USERS_SIGNUP_FORM', 'userflow.forms.signup.SignupForm',
            auto_import=True),
    setting('USERS_SIGNIN_FORM', 'userflow.forms.signin.SigninForm',
            auto_import=True),

    setting('USERS_SIGNIN_ON_EMAIL_CONFIRM', True),

    setting('USERS_SITE_URL', utils.dummy_site_url),
    setting('USERS_SITE_NAME', utils.dummy_site_name),

    setting('USERS_DUMMY_EMAIL', None),

    setting('USERS_CONFIRMATION_EXPIRATION', datetime.timedelta(days=3)),

)


class Wrapper(object):
    def __init__(self, wrapped):
        super(Wrapper, self).__init__()
        self.wrapped = wrapped

    def run_flow(self, flow, *args, **kwargs):
        flow_actions = getattr(self, flow)
        for action in flow_actions:
            result = action(*args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            if result and isinstance(result, dict):
                kwargs.update(result)
        raise ImproperlyConfigured()

    def get_site_url(self, request):
        site_url = self.USERS_SITE_URL
        if callable(site_url):
            return site_url(request)
        return site_url

    def get_site_name(self, request):
        site_name = self.USERS_SITE_NAME
        if callable(site_name):
            return site_name(request)
        return site_name

    def __getattribute__(self, name):
        try:
            return super(Wrapper, self).__getattribute__(name)
        except AttributeError:
            return self.wrapped.SETTINGS[name]

sys.modules[__name__] = Wrapper(sys.modules[__name__])
