# encoding: utf-8

from django.http.response import Http404, HttpResponse
from django.views.generic.detail import DetailView

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
