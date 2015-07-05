# encoding: utf-8

from django.contrib.auth import get_user_model
from django import forms
from django.forms.models import modelformset_factory

from userflow import models


__all__ = ()


class PersonalForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = 'name', 'real_name', 'birthday', 'gender', 'location',


class AboutForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = 'about',


class EmailForm(forms.ModelForm):
    class Meta:
        model = models.UserEmail
        fields = 'email', 'is_public',


BaseEmailsFormset = modelformset_factory(models.UserEmail,
                                         EmailForm,
                                         can_delete=True)


class EmailsFormset(BaseEmailsFormset):
    pass


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = 'type', 'value',


BaseContactsFormset = modelformset_factory(models.Contact,
                                           ContactForm,
                                           can_delete=True)


class ContactsFormset(BaseContactsFormset):
    pass
