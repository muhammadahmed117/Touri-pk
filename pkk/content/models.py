from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from taggit.managers import TaggableManager

User = get_user_model()

# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='Pakistan')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')],
        default='easy'
    )
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    min_days = models.PositiveIntegerField(default=1)
    max_capacity = models.PositiveIntegerField(default=50)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_reviews_count(self):
        return self.reviews.count()

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.destination.name} - {self.caption or 'Image'}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('food', 'Food & Beverages'),
        ('handicrafts', 'Handicrafts'),
        ('books', 'Books & Media'),
        ('accessories', 'Accessories'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='handicrafts')
    stock_quantity = models.PositiveIntegerField(default=0)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, help_text='Weight in kilograms')
    company = models.ForeignKey('packages.Company', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    is_approved = models.BooleanField(default=True, help_text='Products added by companies require admin approval')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    
    class Meta:
        ordering = ['created_at']  # FIFO queue: oldest first
    
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        reviews = self.product_reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def is_in_stock(self):
        return self.stock_quantity > 0

class CostComponent(models.Model):
    CATEGORY_CHOICES = [
        ('camping', 'Camping & Accommodation'),
        ('transport', 'Transportation'),
        ('food', 'Food & Dining'),
        ('activities', 'Activities & Tours'),
        ('shopping', 'Shopping'),
        ('misc', 'Miscellaneous')
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='cost_components')
    
    def __str__(self):
        return f"{self.name} - {self.destination.name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    images = models.ImageField(upload_to='reviews/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'destination']
    
    def __str__(self):
        return f"{self.user.username} - {self.destination.name} ({self.rating}/5)"

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'destination']
    
    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"

class TravelTip(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='travel_tips')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_tips')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.destination.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart - {self.user.username}"
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_items_count(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_total_weight(self):
        """Calculate total weight of all items in cart (in kg)"""
        from decimal import Decimal
        total = Decimal('0')
        for item in self.items.all():
            weight = item.get_weight()
            if weight > 0:
                total += weight
        return total
    
    def get_shipping_fee(self):
        """Calculate shipping fee based on total weight
        - ≤2kg: 200 PKR
        - >2kg: 200 + (50 × extra kg)
        """
        from decimal import Decimal
        total_weight = self.get_total_weight()
        
        if total_weight <= 0:
            return Decimal('200.00')  # Default shipping if no weight
        
        if total_weight <= 2:
            return Decimal('200.00')
        
        # Calculate extra weight beyond 2kg
        extra_weight = total_weight - Decimal('2')
        # Round up to next kg for extra weight
        import math
        extra_kg = math.ceil(float(extra_weight))
        
        shipping_fee = Decimal('200.00') + (Decimal('50.00') * extra_kg)
        return shipping_fee

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def get_weight(self):
        """Calculate total weight of this cart item (in kg)"""
        from decimal import Decimal
        return Decimal(str(self.product.weight_kg)) * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_orders')
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Shipping Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    
    # Order Details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of order
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_subtotal(self):
        return self.price * self.quantity


class CustomPackageOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed by Admin'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    VEHICLE_CHOICES = [
        ('grand-cabin', 'Grand Cabin (7-13 people)'),
        ('coaster', 'Coaster (14-27 people)'),
    ]
    
    FOOD_CHOICES = [
        ('both', 'Breakfast & Dinner'),
        ('breakfast', 'Breakfast Only'),
        ('dinner', 'Dinner Only'),
        ('none', 'No Food'),
    ]
    
    ACCOMMODATION_CHOICES = [
        ('luxury', 'Luxury'),
        ('delux', 'Delux'),
        ('standard', 'Standard'),
    ]
    
    # Order reference
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_package_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Package details
    destination = models.CharField(max_length=100)
    num_days = models.PositiveIntegerField()
    num_people = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
    vehicle = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    food = models.CharField(max_length=20, choices=FOOD_CHOICES)
    accommodation = models.CharField(max_length=20, choices=ACCOMMODATION_CHOICES)
    guide = models.BooleanField(default=False)
    bonfire = models.BooleanField(default=False)
    
    # Pricing
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    per_person_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Payment
    payment_status = models.CharField(max_length=20, default='unpaid', choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ])
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']  # FIFO queue: oldest first
    
    def __str__(self):
        return f"Custom Package #{self.order_number} - {self.destination} ({self.user.username})"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = 'CP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)


class AdminNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('custom_package', 'New Custom Package Request'),
        ('payment', 'Payment Received'),
        ('order', 'New Product Order'),
        ('general', 'General'),
    ]
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional reference to the related order
    custom_package_order = models.ForeignKey(
        CustomPackageOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications'
    )
    
    class Meta:
        ordering = ['created_at']  # FIFO queue: oldest first
    
    def __str__(self):
        return f"[{self.notification_type}] {self.title}"
