# encoding: utf-8

from django.contrib.auth import models as auth_models
from django.db import models
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _

from userflow import conf
from userflow.models.emails import UserEmail


__all__ = 'BaseUser',


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
                                   user=user)
            user_email.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
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

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.name or self.get_short_name()

    def get_short_name(self):
        return self.email

    @property
    def email(self):
        # compat
        user_email = self.primary_email
        if user_email:
            return user_email.email
        return conf.USERS_DUMMY_EMAIL

    def has_usable_email(self):
        return self.email != conf.USERS_DUMMY_EMAIL

    @property
    def primary_email(self):
        user_email = self.emails.filter(is_primary=True).first() or \
                     self.emails.first()
        return user_email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
