# encoding: utf-8

from django.views.generic.edit import FormMixin

from userflow.models import PasswordResetConfirmation
from userflow.views.base import ConfirmView
from userflow import forms


__all__ = 'SetPasswordView',


class SetPasswordView(FormMixin, ConfirmView):
    model = PasswordResetConfirmation
    template_name = 'userflow/reset/change.html'
    form_class = forms.password.SetPasswordForm

    def is_valid_confirmation(self):
        return self.object and \
               self.object.confirm_key == self.kwargs.get('key')

    def form_valid(self, form):
        if self.object:
            form.user = self.object.email.user
            form.save()
            self.object.confirm()
        return self.render_to_response(self.get_context_data(form=form,
                                                             object=self.object))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,
                                                             object=self.object))

    def get_form_kwargs(self):
        kwargs = super(SetPasswordView, self).get_form_kwargs()
        kwargs.update({
            'user': None,
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object,
                                        form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
