# encoding: utf-8

from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


__all__ = ()


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    def __init__(self, *args, **kwargs):
        self.user_cache = None
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


class PasswordSetForm(auth_forms.SetPasswordForm):
    pass


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    pass


def get_password_form(user):
    if user.has_usable_password():
        return PasswordChangeForm
    return PasswordSetForm
