# encoding: utf-8

from collections import OrderedDict

from userflow import forms
from userflow.views.base import MultiformView


__all__ = 'EmailAddView', 'PasswordChangeView',


class ProfileEditView(MultiformView):
    form_classes = OrderedDict((
        ('change-password', forms.password.PasswordChangeForm),
        ('set-password', forms.password.SetPasswordForm),
        # ('add-email', None),
    ))
    template_name = 'userflow/profile/edit.html'

    def get_context_data(self, **kwargs):
        kwargs['emails'] = self.request.user.emails
        return super(ProfileEditView, self).get_context_data(**kwargs)


class EmailAddView(ProfileEditView):
    pass


class PasswordChangeView(ProfileEditView):
    active_form = 'change-password'
