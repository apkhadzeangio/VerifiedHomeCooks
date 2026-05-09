from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils import timezone

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
    actions = ('mark_available', 'mark_unavailable', 'suspend_selected_cooks')

    @admin.action(description='Mark selected cooks available')
    def mark_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description='Mark selected cooks unavailable')
    def mark_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    @admin.action(description='Suspend selected cooks')
    def suspend_selected_cooks(self, request, queryset):
        for cook in queryset.select_related('verification'):
            cook.verification_status = CookProfile.VerificationStatus.SUSPENDED
            cook.is_available = False
            cook.save(update_fields=['verification_status', 'is_available'])
            if hasattr(cook, 'verification'):
                cook.verification.status = CookVerification.Status.SUSPENDED
                cook.verification.reviewed_at = timezone.now()
                cook.verification.reviewed_by = request.user
                cook.verification.save(update_fields=['status', 'reviewed_at', 'reviewed_by'])


@admin.register(CookVerification)
class CookVerificationAdmin(admin.ModelAdmin):
    list_display = ('cook', 'full_name', 'status', 'get_delivery_zone', 'submitted_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status', 'cook__delivery_zone', 'submitted_at', 'reviewed_at')
    search_fields = ('full_name', 'cook__display_name', 'cook__user__username', 'cook__user__email', 'cook__phone_number')
    readonly_fields = ('submitted_at',)
    actions = ('approve_selected', 'reject_selected', 'suspend_selected')

    @admin.display(description='Delivery Zone')
    def get_delivery_zone(self, obj):
        return obj.cook.delivery_zone

    @admin.action(description='Approve selected cook applications')
    def approve_selected(self, request, queryset):
        now = timezone.now()
        for verification in queryset.select_related('cook', 'cook__user'):
            verification.status = CookVerification.Status.APPROVED
            verification.reviewed_at = now
            verification.reviewed_by = request.user
            verification.save(update_fields=['status', 'reviewed_at', 'reviewed_by'])

            cook = verification.cook
            cook.verification_status = CookProfile.VerificationStatus.APPROVED
            cook.is_available = True
            cook.save(update_fields=['verification_status', 'is_available'])

            user = cook.user
            user.role = User.Roles.COOK
            user.save(update_fields=['role'])

    @admin.action(description='Reject selected cook applications')
    def reject_selected(self, request, queryset):
        now = timezone.now()
        for verification in queryset.select_related('cook', 'cook__user'):
            verification.status = CookVerification.Status.REJECTED
            verification.reviewed_at = now
            verification.reviewed_by = request.user
            verification.save(update_fields=['status', 'reviewed_at', 'reviewed_by'])

            cook = verification.cook
            cook.verification_status = CookProfile.VerificationStatus.REJECTED
            cook.is_available = False
            cook.save(update_fields=['verification_status', 'is_available'])

            user = cook.user
            user.role = User.Roles.CUSTOMER
            user.save(update_fields=['role'])

    @admin.action(description='Suspend selected cooks')
    def suspend_selected(self, request, queryset):
        now = timezone.now()
        for verification in queryset.select_related('cook', 'cook__user'):
            verification.status = CookVerification.Status.SUSPENDED
            verification.reviewed_at = now
            verification.reviewed_by = request.user
            verification.save(update_fields=['status', 'reviewed_at', 'reviewed_by'])

            cook = verification.cook
            cook.verification_status = CookProfile.VerificationStatus.SUSPENDED
            cook.is_available = False
            cook.save(update_fields=['verification_status', 'is_available'])
    list_display = ('cook', 'full_name', 'status', 'submitted_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status', 'submitted_at', 'reviewed_at')
    search_fields = ('full_name', 'cook__user__username', 'cook__phone_number')
    readonly_fields = ('submitted_at',)
