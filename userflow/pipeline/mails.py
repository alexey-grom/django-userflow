# encoding: utf-8

from userflow.mailing import send_mail
from userflow.pipeline.decorators import if_new_user


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
    confirmation = EmailConfirmation.objects.create(email=email)
    confirmation.send('verify', user, request)
