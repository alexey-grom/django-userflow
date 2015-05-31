# encoding: utf-8

from django.db.transaction import atomic
from django.views.generic import FormView
from braces.views import AnonymousRequiredMixin

from userflow import conf


__all__ = 'SignupView',


class SignupView(AnonymousRequiredMixin, FormView):
    template_name = 'userflow/signup.html'

    def get_form_class(self):
        return conf.USERS_SIGNUP_FORM

    def form_valid(self, form):
        with atomic():
            form.user.save()
            return conf.run_flow('USERS_FLOW_UP',
                                 request=self.request,
                                 user=form.user,
                                 is_new=True)
