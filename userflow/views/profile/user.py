# encoding: utf-8

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import DetailView

from userflow.utils import redirect_to_signin


class UserProfileView(DetailView):
    template_name = 'userflow/profile/user.html'
    queryset = get_user_model().objects.active()

    def get_object(self, queryset=None):
        if self.pk_url_kwarg not in self.kwargs:
            return
        return super(UserProfileView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'is_me': self.object == self.request.user,
        })
        return super(UserProfileView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() or \
                      self.request.user

        response = self.check_user(self.object)
        if response:
            return response

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def check_user(self, user):
        is_mine = self.object == self.request.user
        is_long_url = self.pk_url_kwarg in self.kwargs
        is_anon = not self.request.user.is_authenticated()

        if is_long_url and is_mine:
            return HttpResponseRedirect(reverse('users:profile:view'))
        if is_mine and is_anon:
            return redirect_to_signin(self.request)
