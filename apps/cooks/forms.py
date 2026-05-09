from django import forms
from django.db import transaction

from apps.accounts.models import CookProfile, CookVerification, DeliveryZone


class CookApplicationForm(forms.Form):
    display_name = forms.CharField(max_length=150)
    bio = forms.CharField(required=False, widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)
    kitchen_address = forms.CharField(widget=forms.Textarea)
    delivery_zone = forms.ModelChoiceField(queryset=DeliveryZone.objects.filter(is_active=True).order_by('name'))

    full_name = forms.CharField(max_length=255)
    personal_id_number = forms.CharField(max_length=100, required=False)
    id_document_image = forms.ImageField(required=False)
    kitchen_photo = forms.ImageField(required=True)
    additional_kitchen_photo = forms.ImageField(required=False)
    cooking_experience = forms.CharField(widget=forms.Textarea)
    food_safety_notes = forms.CharField(required=False, widget=forms.Textarea)

    @transaction.atomic
    def save(self, user):
        cook_profile = CookProfile.objects.create(
            user=user,
            display_name=self.cleaned_data['display_name'],
            bio=self.cleaned_data['bio'],
            phone_number=self.cleaned_data['phone_number'],
            kitchen_address=self.cleaned_data['kitchen_address'],
            delivery_zone=self.cleaned_data['delivery_zone'],
            verification_status=CookProfile.VerificationStatus.PENDING,
            is_available=False,
        )

        CookVerification.objects.create(
            cook=cook_profile,
            full_name=self.cleaned_data['full_name'],
            personal_id_number=self.cleaned_data['personal_id_number'],
            id_document_image=self.cleaned_data['id_document_image'],
            kitchen_photo=self.cleaned_data['kitchen_photo'],
            additional_kitchen_photo=self.cleaned_data['additional_kitchen_photo'],
            cooking_experience=self.cleaned_data['cooking_experience'],
            food_safety_notes=self.cleaned_data['food_safety_notes'],
            status=CookVerification.Status.PENDING,
        )
        return cook_profile
