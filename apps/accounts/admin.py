from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import CookProfile, CookVerification, CustomerProfile, DeliveryZone, User


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


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'delivery_fee', 'is_active')
    list_filter = ('city', 'is_active')
    search_fields = ('name', 'city')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_phone_number', 'district', 'delivery_zone', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__phone_number', 'district')

    @admin.display(description='Phone Number')
    def get_phone_number(self, obj):
        return obj.user.phone_number


@admin.register(CookProfile)
class CookProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'phone_number', 'delivery_zone', 'verification_status', 'is_available', 'average_rating')
    list_filter = ('verification_status', 'is_available', 'delivery_zone')
    search_fields = ('user__username', 'user__email', 'display_name', 'phone_number')


@admin.register(CookVerification)
class CookVerificationAdmin(admin.ModelAdmin):
    list_display = ('cook', 'full_name', 'status', 'submitted_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status', 'submitted_at', 'reviewed_at')
    search_fields = ('full_name', 'cook__user__username', 'cook__phone_number')
    readonly_fields = ('submitted_at',)
