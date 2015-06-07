# encoding: utf-8

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

from userflow.layout import Link


__all__ = 'SigninForm',


class SigninForm(forms.Form):
    email = forms.EmailField(required=True, label=_('Email'))
    password = forms.CharField(required=True, widget=forms.PasswordInput, label=_('Password'))

    helper = FormHelper()
    helper.form_action = reverse_lazy('users:signin')
    helper.layout = Layout(
        'email', 'password',
        Submit('signin', _('Sign In')),
        Link(reverse_lazy('users:reset-request'), _('Lost your password?')),
    )

    error_messages = {
        'invalid_login': _('Please enter a correct %(username)s and password. '
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
        except forms.ValidationError, e:
            self.add_error('email', e)

        return self.cleaned_data

    @property
    def username_field(self):
        model = get_user_model()
        username_field = model.USERNAME_FIELD
        return get_user_model()._meta.get_field(username_field)

    def check_user(self, email=None, password=None, **kwargs):
        credentials = {self.username_field.name: email,
                       'password': password}
        user = auth.authenticate(**credentials)

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
