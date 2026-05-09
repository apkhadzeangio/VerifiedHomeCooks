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
