# encoding: utf-8

from django.http.response import HttpResponseRedirect

from userflow.pipeline.decorators import if_new_user


def activate_by_default(request, is_new=False, data=None, **kwargs):
    if not is_new or not data:
        return
    data.update({
        'is_active': True,
    })


@if_new_user
def activate_by_email_confirm(request, is_new=False, user=None, **kwargs):
    from userflow.models import EmailConfirmation
    email = user.primary_email
    if email.is_dummy:
        return
    confirmation = EmailConfirmation.objects.create(email=email)
    return HttpResponseRedirect(confirmation.get_wait_url())
