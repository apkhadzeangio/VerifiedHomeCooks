from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomerProfile, DeliveryZone, User


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.CUSTOMER
        if commit:
            user.save()
            CustomerProfile.objects.get_or_create(user=user)
        return user


class UserLoginForm(AuthenticationForm):
    pass


class CustomerProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomerProfile
        fields = ('first_name', 'last_name', 'phone_number', 'default_address', 'district', 'delivery_zone', 'notes')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['phone_number'].initial = self.user.phone_number
        self.fields['delivery_zone'].queryset = DeliveryZone.objects.filter(is_active=True).order_by('name')

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.phone_number = self.cleaned_data['phone_number']
        if commit:
            self.user.save()
            profile.save()
        return profile
