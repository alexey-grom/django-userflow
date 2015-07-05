# encoding: utf-8

from django import template
from userflow.gravatar import Gravatar


register = template.Library()


@register.simple_tag
def gravatar(email, **options):
    return Gravatar(email, **options).url
