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


@if_new_user
def signup_email(request, user=None, is_new=False, **kwargs):
    send_mail(user.email,
              email_template='signup',
              request=request,
              context={'user': user})


@if_new_user
def email_verify(request, user=None, is_new=False, **kwargs):
    from userflow.models import EmailConfirmation
    email = user.primary_email
    if email.is_dummy:
        return
    confirmation = EmailConfirmation(email=email)
    confirmation.send('verify', user, request)
