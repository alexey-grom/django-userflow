# encoding: utf-8

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model

from userflow import signals


def signin(request, user=None, is_new=False, **kwargs):
    if is_new:
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
    auth.login(request, user)

    signals.user_signin.send(get_user_model(), user=user)


def signup(request, is_new=False, data=None, **kwargs):
    if not is_new:
        return

    user = get_user_model().objects.create_user(**data)

    signals.user_signup.send(get_user_model(), user=user)

    return {'user': user}


def signout(request, **kwargs):
    auth.logout(request)

    signals.user_signout.send(get_user_model(), user=request.user)
