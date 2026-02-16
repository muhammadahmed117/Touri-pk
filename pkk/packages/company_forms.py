from django import forms
from django.core.exceptions import ValidationError
from .models import Company
import re


class CompanyRegistrationForm(forms.ModelForm):
    """Form for registering a new tour company with proper validation"""

    class Meta:
        model = Company
        fields = ['name', 'description', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name',
                'maxlength': '200',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your tour company and services...',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'company@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+92 300 1234567',
            }),
        }

    def clean_name(self):
        """Validate company name: must contain letters, no pure numbers"""
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError('Company name is required.')

        if len(name) < 3:
            raise ValidationError('Company name must be at least 3 characters long.')

        if len(name) > 200:
            raise ValidationError('Company name cannot exceed 200 characters.')

        # Must contain at least one letter
        if not re.search(r'[a-zA-Z]', name):
            raise ValidationError('Company name must contain at least one letter. It cannot be all numbers.')

        # Only allow letters, numbers, spaces, &, -, and .
        if not re.match(r'^[a-zA-Z0-9\s&\-\.]+$', name):
            raise ValidationError('Company name can only contain letters, numbers, spaces, &, hyphens, and periods.')

        return name

    def clean_description(self):
        """Validate description has meaningful content"""
        description = self.cleaned_data.get('description', '').strip()

        if not description:
            raise ValidationError('Description is required.')

        if len(description) < 20:
            raise ValidationError('Description must be at least 20 characters long. Please provide more detail about your company.')

        return description

    def clean_email(self):
        """Validate email format and uniqueness"""
        email = self.cleaned_data.get('email', '').lower().strip()

        if not email:
            raise ValidationError('Email is required.')

        # Check domain has a dot (basic sanity check beyond Django's EmailField)
        domain = email.split('@')[-1]
        if domain.count('.') == 0:
            raise ValidationError('Please enter a valid email address with a proper domain.')

        return email

    def clean_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone', '').strip()

        if not phone:
            raise ValidationError('Phone number is required.')

        # Remove common formatting characters for validation
        cleaned_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # Must match phone pattern: optional + followed by 9-15 digits
        if not re.match(r'^\+?\d{9,15}$', cleaned_phone):
            raise ValidationError(
                'Please enter a valid phone number (9-15 digits). '
                'Example: +923001234567 or 03001234567'
            )

        return phone
