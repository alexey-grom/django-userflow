# encoding: utf-8

from django.dispatch.dispatcher import Signal


user_registered = Signal(providing_args='user', )
user_logged_in = Signal(providing_args='user', )
