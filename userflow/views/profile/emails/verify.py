# encoding: utf-8

from django.db.transaction import atomic
from django.http.response import HttpResponseRedirect

from userflow.models.confirm import EmailConfirmation
from userflow.views.profile.emails.base import BaseUserEmailView


class VerifyView(BaseUserEmailView):
    active_state = False

    @atomic
    def render_to_response(self, context, **response_kwargs):
        confirmation, _ = EmailConfirmation.objects.get_or_create(email=self.object)
        confirmation.send('verify', self.request.user, self.request)
        return HttpResponseRedirect(confirmation.get_wait_url())
