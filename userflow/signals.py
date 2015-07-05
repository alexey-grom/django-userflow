# encoding: utf-8

from django.dispatch.dispatcher import Signal


user_signup = Signal(providing_args='user', )
user_signin = Signal(providing_args='user', )
user_signout = Signal(providing_args='user', )

user_email_confirmed = Signal(providing_args='user', )
user_password_changed = Signal(providing_args='user', )
