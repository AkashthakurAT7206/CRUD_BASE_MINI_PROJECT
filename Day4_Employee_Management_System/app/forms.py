from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'department', 'position', 'salary', 'date_joined', 'is_active']
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }
