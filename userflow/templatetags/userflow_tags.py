# encoding: utf-8

import re
from datetime import date

from django import template

from userflow import conf


register = template.Library()

email_hide_regex = re.compile(r'(.?)(.+)')
email_hide_repl = lambda m: (m.group(1) or '') + u'×' * len(m.group(2) or '')


@register.assignment_tag
def get_signin_form():
    return conf.USERS_SIGNIN_FORM()


@register.assignment_tag
def get_signup_form():
    return conf.USERS_SIGNUP_FORM()


@register.filter
def hidden_email(email):
    parts = (email or '').split('@', 1)
    parts = parts or ['', ]
    parts[0] = email_hide_regex.sub(email_hide_repl, parts[0])
    return u'@'.join(parts)


@register.filter
def age(value):
    today = date.today()
    return today.year - \
           value.year - \
           ((today.month, today.day) < (value.month, value.day))
