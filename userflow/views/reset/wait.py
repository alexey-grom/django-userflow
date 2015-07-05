# encoding: utf-8

from userflow.models import PasswordResetConfirmation
from userflow.views.base import ConfirmView


class ResetWaitView(ConfirmView):
    model = PasswordResetConfirmation
    template_name = 'userflow/reset/wait.html'

    def is_valid_confirmation(self):
        return self.object and \
               self.object.wait_key == self.kwargs.get('key')
