from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from orders.constants import STATE_CHOICES
from .models import FeedBack, UserAddress

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['subject', 'message']


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'address_line',
            'city',
            'state',
            'zip_code',
            'country',
            'phone_number',
        ]
        widgets = {
            'address_line': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Street, apartment, landmark'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.Select(choices=STATE_CHOICES, attrs={
                'class': 'form-select'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PIN/ZIP code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone