# encoding: utf-8

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from braces.views import LoginRequiredMixin

from userflow.models.contacts import Contact


class UserContactsMixin(LoginRequiredMixin):
    model = Contact

    def get_queryset(self):
        qs = super(UserContactsMixin, self).\
            get_queryset().\
            filter(user=self.request.user)
        return qs

    def contacts_list_url(self):
        return reverse('users:profile:edit') + \
               '#contacts'

    def redirect_to_contacts(self):
        return HttpResponseRedirect(self.contacts_list_url())
