# encoding: utf-8

from django.views.generic.base import TemplateView


class ResetWaitView(TemplateView):
    template_name = 'userflow/reset/wait.html'
