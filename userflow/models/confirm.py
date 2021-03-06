# encoding: utf-8

from hashlib import sha256 as sha

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from userflow import conf, signals
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

    def get_owner(self):
        raise NotImplementedError

    def get_email(self):
        raise NotImplementedError

    def get_context(self, user):
        return {'user': user,
                'confirmation': self, }

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
        data = repr((settings.SECRET_KEY,
                     self.get_key_params(),
                     args,
                     kwargs))
        result.update(data.encode('utf-8'))
        return result.hexdigest()

    def confirm(self):
        self.is_done = True
        self.save()

    def send(self, email_template, user, request=None):
        context = self.get_context(user)
        send_mail(self.get_email(),
                  email_template=email_template,
                  request=request,
                  context=context)

    class Meta:
        app_label = 'userflow'
        abstract = True


class EmailConfirmation(Confirmation):
    email = models.ForeignKey('UserEmail', related_name='confirmations')

    def get_owner(self):
        return self.email.user

    def get_email(self):
        return self.email.email

    def get_context(self, user):
        context = super(EmailConfirmation, self).get_context(user)
        context.update({
            'is_first': not user.emails.active().exists(),
        })
        return context

    def confirm(self):
        self.email.is_active = True
        self.email.save()

        if not self.email.user.is_active:
            # TODO: flow
            get_user_model().objects.\
                filter(pk=self.email.user_id).\
                update(is_active=True)

        super(EmailConfirmation, self).confirm()
        signals.user_email_confirmed.\
            send(EmailConfirmation, user=self.email.user)

    def get_key_params(self):
        return super(EmailConfirmation, self).get_key_params() + \
               (self.email_id, )

    @models.permalink
    def get_absolute_url(self):
        return 'users:verify:confirm', (), {
            'pk': self.pk,
            'key': self.confirm_key,
        }

    @models.permalink
    def get_wait_url(self):
        return 'users:verify:wait', (), {
            'pk': self.pk,
            'key': self.wait_key,
        }

    class Meta:
        app_label = 'userflow'


class PasswordResetConfirmation(Confirmation):
    email = models.ForeignKey('UserEmail')

    def get_owner(self):
        return self.email.user

    def get_email(self):
        return self.email.email

    def confirm(self):
        super(PasswordResetConfirmation, self).confirm()
        signals.user_password_changed.\
            send(PasswordResetConfirmation, user=self.email.user)

    def get_key_params(self):
        return super(PasswordResetConfirmation, self).get_key_params() + \
               (self.email_id, )

    @models.permalink
    def get_absolute_url(self):
        return 'users:reset:confirm', (), {
            'pk': self.pk,
            'key': self.confirm_key,
        }

    @models.permalink
    def get_wait_url(self):
        return 'users:reset:wait', (), {
            'pk': self.pk,
            'key': self.wait_key,
        }

    class Meta:
        app_label = 'userflow'
