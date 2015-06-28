# encoding: utf-8

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


__all__ = 'SignupForm',


class SignupForm(forms.Form):
    email = forms.EmailField(required=True, label=_('Email'))
    name = forms.CharField(max_length=30, required=True, label=_('Your name'))
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True, label=_('Password'))
    confirm = forms.CharField(widget=forms.PasswordInput, required=True, label=_('Password confirm'))

    helper = FormHelper()
    helper.form_action = reverse_lazy('users:signup')
    helper.add_input(Submit('signup', _('Signup')))

    error_messages = {
        'email_exists': _('This email already exists.'),
        'inactive': _('This account is inactive.'),
        'removed': _('This account is removed.'),
        'password_match': _('Password and confirmation does not match.'),
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data

        if not data:
            return data

        try:
            self.check_user(**data)
        except forms.ValidationError, e:
            self.add_error('email', e)

        try:
            data.pop('confirm', None)
            self.check_passwords(**data)
        except forms.ValidationError, e:
            self.add_error('confirm', e)

        self.user_cache = get_user_model()(**data)

        return data

    def check_user(self, email=None, **kwargs):
        user = None
        try:
            user = get_user_model().objects.get_by_natural_key(email)
        except ObjectDoesNotExist:
            pass

        if user:
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
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )

    def check_passwords(self, password=None, confirm=None, **kwargs):
        if confirm and password and password != confirm:
            raise forms.ValidationError(
                self.error_messages['password_match'],
                code='password_match',
            )

    @property
    def user(self):
        return self.user_cache
