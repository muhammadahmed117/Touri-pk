from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .booking_models import Booking, BookingTraveler
import re


class BookingForm(forms.ModelForm):
    """Form for creating a new booking"""

    # Additional fields for better UX
    agree_terms = forms.BooleanField(
        required=True,
        label="I agree to the terms and conditions"
    )

    class Meta:
        model = Booking
        fields = [
            'travel_date',
            'num_adults',
            'num_children',
            'contact_name',
            'contact_email',
            'contact_phone',
            'emergency_contact',
            'address',
            'city',
            'country',
            'special_requests',
        ]
        widgets = {
            'travel_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': (timezone.now().date() + timedelta(days=1)).isoformat()
            }),
            'num_adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '2'
            }),
            'num_children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+92 300 1234567'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+92 300 1234567'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'Pakistan'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any special requirements, dietary restrictions, or preferences...'
            }),
        }
        labels = {
            'travel_date': 'Departure Date',
            'num_adults': 'Number of Adults (18+ years)',
            'num_children': 'Number of Children (0-17 years)',
            'contact_name': 'Primary Contact Name',
            'contact_email': 'Email Address',
            'contact_phone': 'Phone Number',
            'emergency_contact': 'Emergency Contact Number',
            'special_requests': 'Special Requests (Optional)',
        }

    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop('package', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-fill contact information from user if available
        if self.user and not self.instance.pk:
            if hasattr(self.user, 'full_name') and self.user.full_name:
                self.fields['contact_name'].initial = self.user.full_name
            if self.user.email:
                self.fields['contact_email'].initial = self.user.email

    def clean_travel_date(self):
        travel_date = self.cleaned_data.get('travel_date')

        if travel_date:
            # Must be at least 1 day in the future
            min_date = timezone.now().date() + timedelta(days=1)
            if travel_date < min_date:
                raise ValidationError("Travel date must be at least 1 day from now.")

            # Check package availability if package is provided
            if self.package:
                if self.package.available_from and travel_date < self.package.available_from:
                    raise ValidationError(f"This package is available from {self.package.available_from.strftime('%B %d, %Y')}.")
                if self.package.available_to and travel_date > self.package.available_to:
                    raise ValidationError(f"This package is available until {self.package.available_to.strftime('%B %d, %Y')}.")

        return travel_date

    def clean(self):
        cleaned_data = super().clean()
        num_adults = cleaned_data.get('num_adults', 0)
        num_children = cleaned_data.get('num_children', 0)

        if not num_adults:
            raise ValidationError("At least one adult is required.")

        total_travelers = num_adults + num_children

        # Check package capacity if package is provided
        if self.package:
            if total_travelers < self.package.min_people:
                raise ValidationError(f"This package requires a minimum of {self.package.min_people} travelers.")
            if total_travelers > self.package.max_people:
                raise ValidationError(f"This package allows a maximum of {self.package.max_people} travelers.")

        return cleaned_data

    def clean_contact_name(self):
        """Validate contact name contains only letters"""
        name = self.cleaned_data.get('contact_name', '').strip()
        if name:
            if not re.search(r'[a-zA-Z]', name):
                raise ValidationError('Contact name must contain at least one letter.')
            if not re.match(r'^[a-zA-Z\s\.\-\']+$', name):
                raise ValidationError('Contact name can only contain letters, spaces, hyphens, apostrophes, and periods.')
            if len(name) < 2:
                raise ValidationError('Contact name must be at least 2 characters long.')
        return name

    def clean_contact_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('contact_phone', '').strip()
        if phone:
            cleaned_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not re.match(r'^\+?\d{9,15}$', cleaned_phone):
                raise ValidationError(
                    'Please enter a valid phone number (9-15 digits). '
                    'Example: +923001234567 or 03001234567'
                )
        return phone

    def clean_emergency_contact(self):
        """Validate emergency contact phone number format"""
        phone = self.cleaned_data.get('emergency_contact', '').strip()
        if phone:
            cleaned_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not re.match(r'^\+?\d{9,15}$', cleaned_phone):
                raise ValidationError(
                    'Please enter a valid emergency contact number (9-15 digits). '
                    'Example: +923001234567 or 03001234567'
                )
        return phone

    def clean_city(self):
        """Validate city contains only letters"""
        city = self.cleaned_data.get('city', '').strip()
        if city:
            if not re.match(r'^[a-zA-Z\s\.\-]+$', city):
                raise ValidationError('City name can only contain letters, spaces, hyphens, and periods.')
        return city

    def clean_country(self):
        """Validate country contains only letters"""
        country = self.cleaned_data.get('country', '').strip()
        if country:
            if not re.match(r'^[a-zA-Z\s\.\-]+$', country):
                raise ValidationError('Country name can only contain letters, spaces, hyphens, and periods.')
        return country


class TravelerForm(forms.ModelForm):
    """Form for adding traveler details"""

    class Meta:
        model = BookingTraveler
        fields = [
            'full_name',
            'age',
            'gender',
            'passport_number',
            'cnic_number',
            'dietary_requirements',
            'medical_conditions',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name as per ID'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '150'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Passport number (if applicable)'
            }),
            'cnic_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CNIC number (for Pakistani nationals)'
            }),
            'dietary_requirements': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Vegetarian, Halal, No nuts'
            }),
            'medical_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any medical conditions we should know about'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        passport_number = cleaned_data.get('passport_number')
        cnic_number = cleaned_data.get('cnic_number')

        # At least one ID must be provided
        if not passport_number and not cnic_number:
            raise ValidationError("Please provide either a passport number or CNIC number.")

        return cleaned_data

    def clean_full_name(self):
        """Validate traveler name contains only letters"""
        name = self.cleaned_data.get('full_name', '').strip()
        if name:
            if not re.search(r'[a-zA-Z]', name):
                raise ValidationError('Full name must contain at least one letter.')
            if not re.match(r'^[a-zA-Z\s\.\-\']+$', name):
                raise ValidationError('Full name can only contain letters, spaces, hyphens, apostrophes, and periods.')
            if len(name) < 2:
                raise ValidationError('Full name must be at least 2 characters long.')
        return name


# Formset for managing multiple travelers
from django.forms import inlineformset_factory

TravelerFormSet = inlineformset_factory(
    Booking,
    BookingTraveler,
    form=TravelerForm,
    extra=2,  # Start with 2 empty forms
    max_num=20,  # Maximum 20 travelers
    can_delete=True,
    validate_min=True,
    min_num=1  # At least 1 traveler required
)


class BookingCancellationForm(forms.Form):
    """Form for cancelling a booking"""

    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please provide a reason for cancellation...',
        }),
        label='Cancellation Reason',
        required=True
    )

    confirm = forms.BooleanField(
        required=True,
        label='I understand that cancellation charges may apply'
    )

