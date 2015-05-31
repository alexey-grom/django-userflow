# encoding: utf-8

from django.views.generic.edit import FormView
from braces.views import AnonymousRequiredMixin

from userflow import conf
from userflow.views.base import SignLayoutMixin


__all__ = 'SigninView',


class SigninView(AnonymousRequiredMixin, SignLayoutMixin, FormView):
    template_name = 'userflow/signin.html'

    def get_form_class(self):
        return conf.USERS_SIGNIN_FORM

    def form_valid(self, form):
        return conf.run_flow('USERS_FLOW_UP',
                             request=self.request,
                             user=form.user,
                             is_new=False)
