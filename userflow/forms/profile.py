# encoding: utf-8

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.forms.models import BaseInlineFormSet, BaseModelFormSet, modelformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Row, Layout, Div

from userflow import conf, models


__all__ = 'SigninForm',


class PersonalForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_action = reverse_lazy('users:edit', kwargs={'name': 'personal'})
    helper.add_input(Submit('submit', _('Save')))

    class Meta:
        model = get_user_model()
        fields = 'real_name', 'birthday', 'gender', 'location',


class AboutForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_action = reverse_lazy('users:edit', kwargs={'name': 'about'})
    helper.add_input(Submit('submit', _('Save')))

    class Meta:
        model = get_user_model()
        fields = 'about',


# class EmailForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(EmailForm, self).__init__(*args, **kwargs)
#         helper = FormHelper()
#         helper.form_tag = False
#         helper.layout = Layout(
#             Row(),
#         )
#         self.helper = helper
#
#     class Meta:
#         model = models.UserEmail
#         fields = 'email', 'is_primary', 'is_public',
#
#
# BaseEmailsFormset = modelformset_factory(models.UserEmail,
#                                          EmailForm,
#                                          can_delete=True)
#
#
# class EmailsFormset(BaseEmailsFormset):
#     def __init__(self, *args, **kwargs):
#         super(EmailsFormset, self).__init__(*args, **kwargs)
#         helper = FormHelper()
#         helper.form_action = reverse_lazy('users:edit',
#                                           kwargs={'name': 'emails'})
#         helper.add_input(Submit('submit', _('Save')))
#         self.helper = helper
#
#
# class ContactForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ContactForm, self).__init__(*args, **kwargs)
#         helper = FormHelper()
#         helper.form_tag = False
#         helper.layout = Layout(
#             Row(Div(''),),
#         )
#         self.helper = helper
#
#     class Meta:
#         model = models.Contact
#         fields = 'type', 'value',
#
#
# BaseContactsFormset = modelformset_factory(models.Contact,
#                                            ContactForm,
#                                            can_delete=True)
#
#
# class ContactsFormset(BaseContactsFormset):
#     def __init__(self, *args, **kwargs):
#         super(ContactsFormset, self).__init__(*args, **kwargs)
#         helper = FormHelper()
#         helper.form_action = reverse_lazy('users:edit',
#                                           kwargs={'name': 'contacts'})
#         helper.add_input(Submit('submit', _('Save')))
#         self.helper = helper
