# encoding: utf-8

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from userflow.models import UserEmail, Contact


class UserEmailInline(admin.TabularInline):
    model = UserEmail


class ContactInline(admin.TabularInline):
    model = Contact


class UserAdmin(auth_admin.UserAdmin):
    list_display = 'id', 'email', 'name', 'is_staff', 'is_superuser',
    search_fields = 'email', 'name', 'email',
    ordering = '-id',
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('password', )}),
        (_('Personal info'), {'fields': ('email', 'name', 'real_name',
                                         'birthday', 'gender', 'location',
                                         'about', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = 'email',
    inlines = UserEmailInline, ContactInline,


UserModel = get_user_model()
if admin.site.is_registered(UserModel):
    admin.site.unregister(UserModel)
admin.site.register(get_user_model(), UserAdmin)
