# encoding: utf-8

from django.db.transaction import atomic
from django.views.generic import FormView
from braces.views import AnonymousRequiredMixin

from userflow import conf
from userflow.views.base import SignLayoutMixin


__all__ = 'SignupView',


class SignupView(AnonymousRequiredMixin, SignLayoutMixin, FormView):
    template_name = 'userflow/sign/signup.html'

    def get_form_class(self):
        return conf.USERS_SIGNUP_FORM

    @atomic
    def form_valid(self, form):
        return conf.run_flow('USERS_FLOW_UP',
                             request=self.request,
                             data=form.cleaned_data,
                             user=None,
                             is_new=True)
