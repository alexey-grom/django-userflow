# encoding: utf-8

from django.utils.six import wraps

from userflow.mailing import send_mail


def if_new_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('is_new', False):
            return
        user = kwargs.get('user', None)
        if not user:
            return
        return func(*args, **kwargs)
    return wrapper


def if_has_email(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from userflow import conf
        user = kwargs.get('user', None)
        if user.email == conf.USERS_DUMMY_EMAIL:
            return
        return func(*args, **kwargs)
    return wrapper


@if_new_user
@if_has_email
def signup_email(request, user=None, is_new=False, **kwargs):
    send_mail(user.email,
              email_template='signup',
              request=request,
              context={'user': user})


@if_new_user
@if_has_email
def activate_by_email_verify(request, user=None, is_new=False, **kwargs):
    send_mail(user.email,
              email_template='verify',
              request=request,
              context={'user': user})
