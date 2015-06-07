# encoding: utf-8

from userflow.models import EmailConfirmation
from userflow.views.base import ConfirmView


__all__ = 'ConfirmEmailView',


class ConfirmEmailView(ConfirmView):
    model = EmailConfirmation
    template_name = 'userflow/verify/confirm.html'

    def is_valid_confirmation(self):
        return self.object and \
               self.object.confirm_key == self.kwargs.get('key')

    def success(self):
        self.object.confirm()
        return {}
