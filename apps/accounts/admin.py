from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'phone_number', 'role', 'is_staff', 'is_active')
    fieldsets = DjangoUserAdmin.fieldsets + ((
        'Role & Contact',
        {'fields': ('phone_number', 'role')},
    ),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + ((
        'Role & Contact',
        {'fields': ('email', 'phone_number', 'role')},
    ),)
