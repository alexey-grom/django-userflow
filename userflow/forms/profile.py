# encoding: utf-8

from django.contrib.auth import get_user_model
from django import forms


__all__ = ()


class PersonalForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = 'name', 'real_name', 'birthday', 'gender', 'location',


class AboutForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = 'about',
