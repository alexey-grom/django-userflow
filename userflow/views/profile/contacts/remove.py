# encoding: utf-8

from django.db.transaction import atomic
from django.views.generic.detail import DetailView

from userflow.views.profile.contacts.base import UserContactsMixin


class RemoveView(UserContactsMixin, DetailView):
    @atomic
    def render_to_response(self, context, **response_kwargs):
        self.object.delete()
        return self.redirect_to_contacts()
