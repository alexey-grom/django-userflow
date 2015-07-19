# encoding: utf-8

from django import template
from six import string_types

from userflow import conf
from userflow.psa.utils import get_psa_backends, is_psa_installed


register = template.Library()


@register.assignment_tag
def is_psa_enabled():
    return is_psa_installed()


@register.assignment_tag(name='get_psa_backends')
def psa_backends():
    return get_psa_backends()


@register.assignment_tag(name='get_psa_backend_context')
def psa_backends_context(backend):
    backend_name = backend.name if not isinstance(backend, string_types) else backend
    print(backend_name)
    return conf.USERS_PSA_BACKENDS_CONTEXT.get(backend_name) or {}
