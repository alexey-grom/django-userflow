# encoding: utf-8

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from userflow import forms
from userflow.mailing import send_mail
# from userflow.models import PasswordResetConfirm


class SetPasswordView(FormView, DetailView):
    form_class = forms.password.SetPasswordForm
    template_name = 'userflow/reset/request.html'

    # def form_valid(self, form):
    #     confirm = PasswordResetConfirm.objects.create(user=form.user)
    #     send_mail(form.user.email,
    #               email_template='reset',
    #               request=self.request,
    #               context={'user': form.user,
    #                        'confirm': confirm})
    #     return super(PasswordResetView, self).form_valid(form)
