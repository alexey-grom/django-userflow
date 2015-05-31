# encoding: utf-8

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model

from userflow import signals


def signin(request, user=None, is_new=False, **kwargs):
    if is_new:
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)

    signals.user_logged_in.send(get_user_model(), user=user)


def signup(request, user=None, is_new=False, **kwargs):
    if not is_new:
        return

    signals.user_registered.send(get_user_model(), user=user)


def signout(request, **kwargs):
    auth.logout(request)
