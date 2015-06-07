# encoding: utf-8

from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from userflow.layout import Link


__all__ = 'SetPasswordForm', \
          'PasswordChangeForm',


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    helper = FormHelper()
    helper.form_action = reverse_lazy('users:reset-request')
    helper.layout = Layout(
        'email',
        Submit('submit', _('Submit')),
        Link(reverse_lazy('users:signin'), _('Sign In')),
    )

    def __init__(self, *args, **kwargs):
        self.user_cache =  None
        super(PasswordResetForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.user_cache = get_user_model().objects.\
            filter(emails__email=email).\
            first()
        if not self.user_cache:
            raise ValidationError(_('Can\'t find that email, sorry'))
        return email

    @property
    def user(self):
        return self.user_cache


class SetPasswordForm(auth_forms.SetPasswordForm):
    helper = FormHelper()
    helper.form_action = ''
    helper.add_input(Submit('change', _('Change')))


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    helper = FormHelper()
    helper.form_action = ''
    helper.add_input(Submit('change', _('Change')))
