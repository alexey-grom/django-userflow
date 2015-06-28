# encoding: utf-8

from django.core.exceptions import ImproperlyConfigured
from django.http.response import Http404, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from userflow.models import Confirmation


class LayoutMixin(object):
    default_layout = 'userflow/base.html'
    ajax_layout = 'userflow/modal.html'

    def get_context_data(self, **kwargs):
        layout = self.default_layout
        if self.request.is_ajax():
            layout = self.ajax_layout
        kwargs.setdefault('layout', layout)
        return super(LayoutMixin, self).get_context_data(**kwargs)


class SignLayoutMixin(LayoutMixin):
    default_layout = 'userflow/sign/sign-default.html'
    ajax_layout = 'userflow/sign/sign-ajax.html'


class ConfirmView(DetailView):
    model = Confirmation
    context_object_name = 'confirmation'

    def get_queryset(self):
        return super(ConfirmView, self).get_queryset().unfinished()

    def get_object(self, queryset=None):
        try:
            return super(ConfirmView, self).get_object(queryset)
        except Http404:
            pass

    def is_valid_confirmation(self):
        return self.object and \
               self.object.wait_key == self.kwargs.get('key')

    def render_to_response(self, context, **response_kwargs):
        is_ok = self.is_valid_confirmation()

        context.update({
            self.context_object_name: None if not is_ok else self.object,
        })
        result = self.success() if is_ok else self.fail()

        if result and isinstance(result, HttpResponse):
            return result

        context.update(result)

        return super(ConfirmView, self).render_to_response(context, **response_kwargs)

    def success(self):
        return {}

    def fail(self):
        return {}


# class MultiformView(FormView):
#     form_classes = None
#     active_form = None
#
#     def get_form_classes(self):
#         return (self.form_classes or {}).copy()
#
#     def get_active_form(self):
#         if self.active_form:
#             return self.active_form
#         form_classes = self.get_form_classes()
#         if form_classes:
#             return form_classes.keys()[0]
#         raise ImproperlyConfigured
#
#     def get_form_class(self):
#         return self.get_form_classes().get(self.get_active_form())
#
#     def get_context_data(self, **kwargs):
#         context_data = super(MultiformView, self).get_context_data(**kwargs)
#         kwargs.update(self.get_active_form(), context_data.get('form'))
#         return context_data
