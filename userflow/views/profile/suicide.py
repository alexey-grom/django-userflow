# encoding: utf-8

from django.conf import settings
from django.views.generic.edit import DeleteView

from userflow.utils import redirect_to_signin


class SuicideView(DeleteView):
    template_name = 'userflow/profile/suicide.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect_to_signin(self.request)
        return super(SuicideView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return settings.LOGIN_URL
