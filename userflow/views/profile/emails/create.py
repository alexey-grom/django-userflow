# encoding: utf-8

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import CreateView

from userflow.models.emails import UserEmail
from userflow.views.profile.emails.base import UserEmailsMixin


class AddEmailView(UserEmailsMixin, CreateView):
    model = UserEmail
    fields = 'email',
    template_name = 'userflow/profile/add-email.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddEmailView, self).form_valid(form)

    def get_success_url(self):
        return HttpResponseRedirect(reverse(
            'users:profile:emails:verify',
            kwargs={'pk': self.object.pk}
        ))
