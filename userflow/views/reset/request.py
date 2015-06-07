# encoding: utf-8

from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView

from userflow import forms
from userflow.models import PasswordResetConfirmation


class PasswordResetView(FormView):
    form_class = forms.password.PasswordResetForm
    template_name = 'userflow/reset/request.html'

    def form_valid(self, form):
        email = form.user.emails.\
            filter(email=form.cleaned_data['email']).\
            first()
        confirm = PasswordResetConfirmation.objects.\
            unfinished().\
            filter(email=email).\
            first()
        if not confirm:
            confirm = PasswordResetConfirmation.objects.create(email=email)
        confirm.send('reset', form.user, self.request)
        return HttpResponseRedirect(confirm.get_wait_url())
