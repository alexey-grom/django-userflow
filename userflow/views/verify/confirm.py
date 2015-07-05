# encoding: utf-8
from django.contrib.auth import login

from userflow import conf
from userflow.models import EmailConfirmation
from userflow.views.base import ConfirmView


class ConfirmEmailView(ConfirmView):
    model = EmailConfirmation
    template_name = 'userflow/verify/confirm.html'

    def is_valid_confirmation(self):
        return self.object and \
               not self.object.email.is_active and \
               self.object.confirm_key == self.kwargs.get('key')

    def success(self):
        self.object.confirm()

        if conf.USERS_SIGNIN_ON_EMAIL_CONFIRM:
            user = self.object.get_owner()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)

        return {}
