# encoding: utf-8

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django import forms
from django.utils.translation import ugettext_lazy as _


__all__ = ()


class SigninForm(forms.Form):
    email = forms.EmailField(required=True, label=_('Email'))
    password = forms.CharField(required=True, widget=forms.PasswordInput, label=_('Password'))

    error_messages = {
        'invalid_login': _('Please enter a correct email and password. '
                           'Note that both fields may be case-sensitive.'),
        'inactive': _('This account is inactive.'),
        'removed': _('This account is removed.'),
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(SigninForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data

        try:
            self.user_cache = self.check_user(**data)
        except forms.ValidationError as e:
            self.add_error('email', e)

        return data

    @property
    def username_field(self):
        model = get_user_model()
        username_field = model.USERNAME_FIELD
        return get_user_model()._meta.get_field(username_field)

    def check_user(self, email=None, password=None, **kwargs):
        credentials = {self.username_field.name: email,
                       'password': password}

        try:
            user = auth.authenticate(**credentials)
        except MultipleObjectsReturned:
            return

        if user is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )

        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        if user.is_removed:
            raise forms.ValidationError(
                self.error_messages['removed'],
                code='removed',
            )

        return user

    @property
    def user(self):
        return self.user_cache
