# encoding: utf-8

from django.http.response import HttpResponseRedirect

from userflow.pipeline.decorators import if_new_user


@if_new_user
def activate_account(request, is_new=False, data=None, **kwargs):
    data.update({
        'is_active': True,
    })


@if_new_user
def send_email_confirm(request, is_new=False, user=None, **kwargs):
    from userflow.models import EmailConfirmation
    email = user.primary_email
    if email.is_dummy:
        return
    confirmation = EmailConfirmation.objects.create(email=email)
    confirmation.send('verify', user, request)
    return HttpResponseRedirect(confirmation.get_wait_url())
