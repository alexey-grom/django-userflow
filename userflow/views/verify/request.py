# encoding: utf-8

from django.http.response import HttpResponseRedirect, Http404
from django.views.generic.detail import DetailView

from userflow.models import UserEmail


class RequestConfirmEmailView(DetailView):
    model = UserEmail

    def get_queryset(self):
        return super(RequestConfirmEmailView, self).get_queryset().inactive()

    def get_object(self, queryset=None):
        object = super(RequestConfirmEmailView, self).get_object(queryset)
        if object.user != self.request.user:
            if object.user.is_active:
                raise Http404
        confirmation = object.confirmations.\
            unfinished().\
            first()
        if not confirmation:
            from userflow.models import EmailConfirmation
            confirmation = EmailConfirmation.objects.create(email=object)
        return confirmation

    def render_to_response(self, context, **response_kwargs):
        self.object.send('verify',
                         self.object.get_owner(),
                         self.request)
        return HttpResponseRedirect(self.object.get_wait_url())
