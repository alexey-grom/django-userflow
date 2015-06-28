# encoding: utf-8

from django.views.generic.base import View
from braces.views import LoginRequiredMixin

from userflow import conf


class SignoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return conf.run_flow('USERS_FLOW_DOWN',
                             request=self.request)
