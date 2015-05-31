# encoding: utf-8

from pprint import pprint

from django.conf import settings


def debug(*args, **kwargs):
    if not settings.DEBUG:
        return

    pprint([args, kwargs])
