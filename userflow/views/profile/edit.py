# encoding: utf-8

from collections import OrderedDict

from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import ContextMixin
from django.views.generic.edit import UpdateView

from userflow import forms
from userflow.forms.password import get_password_form
from userflow.utils import redirect_to_signin


class ProfileEditMixin(ContextMixin):
    form_classes = OrderedDict((
        ('personal', lambda request: forms.profile.PersonalForm(instance=request.user)),
        ('about', lambda request: forms.profile.AboutForm(instance=request.user)),
        ('password', lambda request: get_password_form(request.user)(user=request.user)),
    ))
    template_name = 'userflow/profile/edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect_to_signin(self.request)
        return super(ProfileEditMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileEditMixin, self).get_context_data(**kwargs)

        form = context.get('form')

        forms = {}
        for key, form_class in self.form_classes.items():
            forms[key] = form_class(self.request)
            if forms[key].__class__ == form.__class__:
                forms[key] = form

        context.update({
            'forms': forms,
        })

        return context

    def get_success_url(self):
        return reverse_lazy('users:profile:edit')


class PersonalEditView(ProfileEditMixin, UpdateView):
    form_class = forms.profile.PersonalForm

    def get_object(self, queryset=None):
        return self.request.user


class AboutEditView(ProfileEditMixin, UpdateView):
    form_class = forms.profile.AboutForm

    def get_object(self, queryset=None):
        return self.request.user


class PasswordView(ProfileEditMixin, UpdateView):
    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        return get_password_form(self.request.user)

    def get_form_kwargs(self):
        kwargs = super(PasswordView, self).get_form_kwargs()
        if 'instance' in kwargs:
            kwargs['user'] = kwargs['instance']
            del kwargs['instance']
        return kwargs
