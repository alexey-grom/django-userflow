# encoding: utf-8

from django import template

from userflow import conf


register = template.Library()


@register.assignment_tag
def get_signin_form():
    return conf.USERS_SIGNIN_FORM()


@register.assignment_tag
def get_signup_form():
    return conf.USERS_SIGNUP_FORM()
