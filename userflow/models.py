# encoding: utf-8

from hashlib import sha1
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import models as auth_models, get_user_model
from django.db import models
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from userflow import conf


class UserQueryset(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def removed(self):
        return self.filter(is_removed=True)

    def superusers(self):
        return self.filter(is_superuser=True)

    def staff(self):
        return self.filter(is_staff=True)


class UserManager(auth_models.BaseUserManager.from_queryset(UserQueryset)):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        with atomic():
            email = self.normalize_email(email)
            user = self.model(is_staff=is_staff,
                              is_superuser=is_superuser,
                              **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            user_email = UserEmail(email=email,
                                   user=user,
                                   is_active=True)
            user_email.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def get_by_natural_key(self, username):
        qs = self.filter(emails__email=username)
        return qs.get()


class BaseUser(auth_models.AbstractBaseUser,
               auth_models.PermissionsMixin):
    """
    Generic user model
    """

    name = models.CharField(_('display name'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_removed = models.BooleanField(_('removed'), default=False)

    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'id'  # compat

    def get_full_name(self):
        return self.name or self.get_short_name()

    def get_short_name(self):
        return self.email

    @property
    def email(self):
        # compat
        user_email = self.emails.filter(is_primary=True).first() or \
                     self.emails.first()
        if user_email:
            return user_email.email
        return conf.USERS_DUMMY_EMAIL

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class UserEmail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails')
    email = models.EmailField(_('email address'), unique=True, blank=False)

    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('email')
        verbose_name_plural = _('emails')
        unique_together = (
            ('user', 'is_primary'),
        )


if conf.is_generic_user_model:
    class User(BaseUser):
        """
        Common user model implementation
        """


# class ConfirmationQueryset(models.QuerySet):
#     def unexpired(self):
#         return self.filter(created__gte=now() - timedelta(days=1))


# class Confirmation(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     done = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#
#     objects = ConfirmationQueryset.as_manager()
#
#     def key(self):
#         result = sha1()
#         result.update(repr((settings.SECRET_KEY,
#                             self.pk,
#                             self.user_id, )))
#         return result.hexdigest()
#
#     def activate(self):
#         self.done = True
#         self.save()
#
#     class Meta:
#         abstract = True


# class EmailConfirm(Confirmation):
#     email = models.EmailField()
#
#     def activate(self):
#         if get_user_model().filter(email=self.email).exists():
#             self.user.email = self.email
#             self.user.save()
#         return super(EmailConfirm, self).activate()
#
#     @models.permalink
#     def get_absolute_url(self):
#         return 'users:profile', (), {'pk': self.user_id}


# class PasswordResetConfirm(Confirmation):
#     @models.permalink
#     def get_absolute_url(self):
#         return 'users:profile', (), {'pk': self.user_id}
