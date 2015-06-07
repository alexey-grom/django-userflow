# encoding: utf-8

from userflow.models import EmailConfirmation
from userflow.views.base import ConfirmView


__all__ = 'WaitConfirmEmailView',


class WaitConfirmEmailView(ConfirmView):
    model = EmailConfirmation
    template_name = 'userflow/verify/wait.html'

    def is_valid_confirmation(self):
        return self.object and \
               not self.object.email.is_active and \
               self.object.wait_key == self.kwargs.get('key')
