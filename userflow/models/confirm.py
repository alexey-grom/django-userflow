# encoding: utf-8

from hashlib import sha1

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from userflow import conf
from userflow.mailing import send_mail


__all__ = 'Confirmation', 'EmailConfirmation',


class ConfirmationQueryset(models.QuerySet):
    def unexpired(self):
        deadline = now() - conf.USERS_CONFIRMATION_EXPIRATION
        return self.filter(created__gte=deadline)

    def undone(self):
        return self.filter(is_done=False)

    def unfinished(self):
        return self.unexpired().undone()


class Confirmation(models.Model):
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = ConfirmationQueryset.as_manager()

    def get_key_params(self):
        return self.pk,

    @property
    def confirm_key(self):
        return self.key('confirm')

    @property
    def wait_key(self):
        return self.key('wait')

    def key(self, *args, **kwargs):
        result = sha1()
        result.update(repr((settings.SECRET_KEY,
                            self.get_key_params(),
                            args,
                            kwargs)))
        return result.hexdigest()

    def confirm(self):
        self.is_done = True
        self.save()

    def send(self, email_template, user, request=None):
        context = {'user': user,
                   'confirmation': self, }
        send_mail(user.email,
                  email_template=email_template,
                  request=request,
                  context=context)

    class Meta:
        app_label = 'userflow'
        abstract = True


class EmailConfirmation(Confirmation):
    email = models.ForeignKey('UserEmail', related_name='confirmations')

    def confirm(self):
        self.email.is_active = True
        self.email.save()
        super(EmailConfirmation, self).confirm()

    def get_key_params(self):
        return super(EmailConfirmation, self).get_key_params() + \
               (self.email.email, )

    @models.permalink
    def get_absolute_url(self):
        return 'users:verify-confirm', (), {
            'pk': self.pk,
            'key': self.confirm_key,
        }

    @models.permalink
    def get_wait_url(self):
        return 'users:verify-wait', (), {
            'pk': self.pk,
            'key': self.wait_key,
        }

    class Meta:
        app_label = 'userflow'
