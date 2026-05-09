from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        COOK = 'COOK', 'Cook'
        ADMIN = 'ADMIN', 'Admin'

    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CUSTOMER)

    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.role = self.Roles.ADMIN
        elif not self.role:
            self.role = self.Roles.CUSTOMER
        super().save(*args, **kwargs)

    @property
    def has_cook_profile(self):
        return hasattr(self, 'cook_profile')


class DeliveryZone(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=120, default='Tbilisi')
    description = models.TextField(blank=True)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    default_address = models.TextField(blank=True)
    district = models.CharField(max_length=120, blank=True)
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CustomerProfile<{self.user.username}>"


class CookProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cook_profile')
    display_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='cook_profiles/', blank=True)
    phone_number = models.CharField(max_length=20)
    kitchen_address = models.TextField()
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.PROTECT, related_name='cooks')
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
    is_available = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name


class CookVerification(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    cook = models.OneToOneField(CookProfile, on_delete=models.CASCADE, related_name='verification')
    full_name = models.CharField(max_length=255)
    personal_id_number = models.CharField(max_length=100, blank=True)
    id_document_image = models.ImageField(upload_to='cook_verification/id_documents/', blank=True)
    kitchen_photo = models.ImageField(upload_to='cook_verification/kitchen_photos/')
    additional_kitchen_photo = models.ImageField(upload_to='cook_verification/kitchen_photos/', blank=True)
    cooking_experience = models.TextField(blank=True)
    food_safety_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_cook_verifications')
    admin_comment = models.TextField(blank=True)

    def __str__(self):
        return f"Verification<{self.cook.display_name}>"
