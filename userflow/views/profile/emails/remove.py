# encoding: utf-8

from django.db.transaction import atomic
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from userflow.views.profile.emails.base import BaseUserEmailView


class RemoveView(BaseUserEmailView):
    @atomic
    def render_to_response(self, context, **response_kwargs):
        if self.request.user.emails.active().count() > 1:
            self.object.delete()
        else:
            messages.error(self.request, _(u'You can\'t remove last email'))
        return self.redirect_to_emails()
