# encoding: utf-8

from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from braces.views import LoginRequiredMixin

from userflow.models.emails import UserEmail


class UserEmailsMixin(LoginRequiredMixin):
    model = UserEmail
    active_state = None

    def get_queryset(self):
        qs = super(UserEmailsMixin, self).\
            get_queryset().\
            filter(user=self.request.user)
        if self.active_state is not None:
            qs = qs.filter(is_active=self.active_state)
        return qs

    def emails_list_url(self):
        return reverse('users:profile:edit') + \
               '#emails'

    def redirect_to_emails(self):
        return HttpResponseRedirect(self.emails_list_url())


class BaseUserEmailView(UserEmailsMixin, DetailView):
    pass
