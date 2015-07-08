# encoding: utf-8

from django.views.generic.edit import CreateView

from userflow.models.contacts import Contact
from userflow.views.profile.contacts.base import UserContactsMixin


class AddContactView(UserContactsMixin, CreateView):
    model = Contact
    fields = 'type', 'value',
    template_name = 'userflow/profile/add-contact.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddContactView, self).form_valid(form)

    def get_success_url(self):
        return self.contacts_list_url()
