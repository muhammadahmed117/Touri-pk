from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.conf import settings
import random
import string


class Company(models.Model):
    """Tour company/operator model"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_companies', null=True, blank=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='companies/', blank=True, null=True)
    website = models.URLField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    # Approval system fields
    approval_status = models.CharField(max_length=20, default='pending', choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    approved_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    registration_document = models.FileField(upload_to='companies/documents/', blank=True, null=True)
    cnic_front = models.ImageField(upload_to='companies/cnic/', blank=True, null=True, verbose_name='CNIC Front')
    cnic_back = models.ImageField(upload_to='companies/cnic/', blank=True, null=True, verbose_name='CNIC Back')
    
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['created_at']  # FIFO queue: oldest first

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('packages:company_detail', kwargs={'slug': self.slug})


class Package(models.Model):
    """Tour package model"""
    PACKAGE_TYPES = [
        ('family', 'Family Tour'),
        ('adventure', 'Adventure'),
        ('honeymoon', 'Honeymoon'),
        ('group', 'Group Tour'),
        ('luxury', 'Luxury Tour'),
        ('budget', 'Budget Tour'),
        ('cultural', 'Cultural Tour'),
        ('religious', 'Religious Tour'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES, default='family')
    
    # Destinations - can link to existing destinations
    destination_names = models.CharField(max_length=500, help_text="Comma-separated list of destinations")
    
    # Duration
    duration_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration_nights = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    child_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    
    # Package details
    inclusions = models.TextField(help_text="What's included in the package (one item per line)", blank=True, default='')
    exclusions = models.TextField(help_text="What's not included (one item per line)", blank=True)
    itinerary = models.TextField(help_text="Day-by-day itinerary", blank=True)
    
    # Capacity
    min_people = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1)])
    max_people = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    
    # Media
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    
    # Availability
    available_from = models.DateField(blank=True, null=True)
    available_to = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    # Metadata
    views_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # FIFO queue: oldest first

    def __str__(self):
        return f"{self.name} - {self.company.name}"

    def get_absolute_url(self):
        return reverse('packages:package_detail', kwargs={'slug': self.slug})

    def get_inclusions_list(self):
        """Return inclusions as a list"""
        return [item.strip() for item in self.inclusions.split('\n') if item.strip()]

    def get_exclusions_list(self):
        """Return exclusions as a list"""
        return [item.strip() for item in self.exclusions.split('\n') if item.strip()]

    def get_destinations_list(self):
        """Return destinations as a list"""
        return [dest.strip() for dest in self.destination_names.split(',') if dest.strip()]

    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    def get_reviews_count(self):
        """Return total number of reviews"""
        return self.reviews.count()


class Booking(models.Model):
    """Booking model for package reservations"""
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Booking Information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    
    # Travel Details
    travel_date = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    
    # Contact Information
    phone = models.CharField(max_length=20)
    special_requests = models.TextField(blank=True, null=True)
    
    # Booking Details
    booking_reference = models.CharField(max_length=20, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, blank=True, default='')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, default='')
    transaction_id = models.CharField(max_length=100, blank=True, default='')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']  # FIFO queue: oldest first
        
    def __str__(self):
        return f"{self.booking_reference} - {self.user.username} - {self.package.name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate unique booking reference
            while True:
                ref = 'BK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not Booking.objects.filter(booking_reference=ref).exists():
                    self.booking_reference = ref
                    break
        super().save(*args, **kwargs)


class PackageReview(models.Model):
    """Review model for tour packages - only after completed booking"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='package_reviews')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'package']

    def __str__(self):
        return f"{self.user.username} - {self.package.name} ({self.rating}/5)"
