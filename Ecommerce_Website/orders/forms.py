from django import forms
from .models import Order, OrderItem
from .constants import STATE_CHOICES


class OrderForm(forms.ModelForm):
    """Form for creating/updating orders"""
    
    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'shipping_city',
            'shipping_state',
            'shipping_zip_code',
            'shipping_country',
            'shipping_phone',
            'payment_method',
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete shipping address'
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'shipping_state': forms.Select(choices=STATE_CHOICES, attrs={
                'class': 'form-select'
            }),
            'shipping_zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ZIP/Postal Code'
            }),
            'shipping_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'type': 'tel'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean_shipping_phone(self):
        phone = self.cleaned_data.get('shipping_phone')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone
    
    def clean_shipping_zip_code(self):
        zip_code = self.cleaned_data.get('shipping_zip_code')
        if zip_code and len(zip_code) < 5:
            raise forms.ValidationError("ZIP code must be at least 5 characters.")
        return zip_code



class OrderItemForm(forms.ModelForm):
    """Form for adding items to an order"""
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1
            }),
            'price': forms.HiddenInput(),
        }
