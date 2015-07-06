# encoding: utf-8

from django.db.transaction import atomic

from userflow.views.profile.emails.base import BaseUserEmailView


class PrimaryUpdateView(BaseUserEmailView):
    active_state = True

    @atomic
    def render_to_response(self, context, **response_kwargs):
        self.get_queryset().\
            update(is_primary=False)
        self.get_queryset().\
            filter(pk=self.object.pk).\
            update(is_primary=True)
        return self.redirect_to_emails()
