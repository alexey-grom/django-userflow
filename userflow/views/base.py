# encoding: utf-8


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
