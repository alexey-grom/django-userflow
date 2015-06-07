# encoding: utf-8

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from userflow import conf
from userflow.models import UserEmail


class UserEmailInline(admin.StackedInline):
    model = UserEmail


class UserAdmin(auth_admin.UserAdmin):
    list_display = 'id', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser',
    search_fields = 'email', 'first_name', 'last_name', 'email',
    ordering = '-id',
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    inlines = UserEmailInline,


if conf.is_generic_user_model:
    admin.register(UserAdmin, get_user_model())
