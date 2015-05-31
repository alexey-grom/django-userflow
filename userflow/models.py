# encoding: utf-8

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class BaseUser(auth_models.AbstractBaseUser,
               auth_models.PermissionsMixin):
    """
    Generic user model
    """

    email = models.EmailField(_('email address'), unique=True, blank=False)

    name = models.CharField(_('display name'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_removed = models.BooleanField(_('removed'), default=False)

    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.name or self.get_short_name()

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


if conf.is_generic_user_model:
    class User(BaseUser):
        """
        Common user model implementation
        """
