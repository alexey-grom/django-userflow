# encoding: utf-8

from django import template

from userflow.psa.utils import get_psa_backends


register = template.Library()


@register.assignment_tag(name='get_psa_backends')
def psa_backends():
    return get_psa_backends()
