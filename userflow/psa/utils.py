# encoding: utf-8

from django.apps import apps
from django.contrib.auth import get_backends
from social.backends.base import BaseAuth


def is_psa_installed():
    try:
        import social
    except ImportError:
        return False

    if apps.is_installed('social.apps.django_app.default'):
        return True

    return False


def get_psa_backends():
    if not is_psa_installed():
        return ()
    return (
        backend
        for backend in get_backends()
        if isinstance(backend, BaseAuth)
    )
