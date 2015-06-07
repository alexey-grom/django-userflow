# encoding: utf-8

from django.dispatch.dispatcher import Signal


user_signup = Signal(providing_args='user', )
user_signin = Signal(providing_args='user', )
user_signout = Signal(providing_args='user', )
