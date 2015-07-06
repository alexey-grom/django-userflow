# encoding: utf-8

from django.db.transaction import atomic

from userflow.views.profile.emails.base import BaseUserEmailView


class PublicUpdateView(BaseUserEmailView):
    active_state = True

    @atomic
    def render_to_response(self, context, **response_kwargs):
        is_public = self.kwargs.get('action', None) == 'public'
        self.get_queryset().\
            filter(pk=self.object.pk).\
            update(is_public=is_public)
        return self.redirect_to_emails()
