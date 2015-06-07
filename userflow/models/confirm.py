# encoding: utf-8

from hashlib import sha256 as sha

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from userflow import conf
from userflow.mailing import send_mail


__all__ = 'Confirmation', \
          'EmailConfirmation', \
          'PasswordResetConfirmation',


class ConfirmationQueryset(models.QuerySet):
    def expired(self):
        deadline = now() - conf.USERS_CONFIRMATION_EXPIRATION
        return self.filter(created__lt=deadline)

    def unexpired(self):
        deadline = now() - conf.USERS_CONFIRMATION_EXPIRATION
        return self.filter(created__gte=deadline)

    def undone(self):
        return self.filter(is_done=False)

    def unfinished(self):
        return self.unexpired().undone()

    def clear_expired(self):
        return self.expired().all().delete()


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
        result = sha()
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
        send_mail(self.email.email,  # todo: getter
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
               (self.email_id, )

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


class PasswordResetConfirmation(Confirmation):
    email = models.ForeignKey('UserEmail')

    def get_key_params(self):
        return super(PasswordResetConfirmation, self).get_key_params() + \
               (self.email_id, )

    @models.permalink
    def get_absolute_url(self):
        return 'users:reset-confirm', (), {
            'pk': self.pk,
            'key': self.confirm_key,
        }

    @models.permalink
    def get_wait_url(self):
        return 'users:reset-wait', (), {
            'pk': self.pk,
            'key': self.wait_key,
        }

    class Meta:
        app_label = 'userflow'
