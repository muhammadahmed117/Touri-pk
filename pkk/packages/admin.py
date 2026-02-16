from django.contrib import admin
from .models import Company, Package, Booking, PackageReview


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'email', 'phone', 'approval_status', 'rating', 'is_active', 'created_at']
    list_filter = ['approval_status', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'phone']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ('created_at',)  # FIFO queue: oldest first
    actions = ['approve_companies']
    
    def approve_companies(self, request, queryset):
        queryset.update(approval_status='approved')
        self.message_user(request, f'{queryset.count()} companies approved.')
    approve_companies.short_description = 'Approve selected companies'


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'package_type', 'duration_days', 'price_per_person', 'is_approved', 'is_active', 'is_featured']
    list_filter = ['is_approved', 'is_active', 'is_featured', 'package_type', 'company', 'created_at']
    search_fields = ['name', 'destination_names', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    ordering = ('created_at',)  # FIFO queue: oldest first
    actions = ['approve_packages']
    
    def approve_packages(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} packages approved.')
    approve_packages.short_description = 'Approve selected packages'
    fieldsets = [
        ('Basic Information', {
            'fields': ['company', 'name', 'slug', 'description', 'package_type', 'image']
        }),
        ('Destinations & Duration', {
            'fields': ['destination_names', 'duration_days', 'duration_nights']
        }),
        ('Pricing', {
            'fields': ['price_per_person', 'child_price']
        }),
        ('Package Details', {
            'fields': ['inclusions', 'exclusions', 'itinerary']
        }),
        ('Capacity', {
            'fields': ['min_people', 'max_people']
        }),
        ('Availability', {
            'fields': ['available_from', 'available_to', 'is_active', 'is_featured', 'is_approved']
        }),
        ('Metadata', {
            'fields': ['views_count', 'rating', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'user', 'package', 'travel_date', 'num_adults', 'num_children', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'travel_date', 'created_at']
    search_fields = ['booking_reference', 'user__username', 'user__email', 'package__name', 'phone']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']
    ordering = ('created_at',)  # FIFO queue: oldest first
    date_hierarchy = 'travel_date'
    
    fieldsets = [
        ('Booking Information', {
            'fields': ['user', 'package', 'booking_reference', 'status']
        }),
        ('Travel Details', {
            'fields': ['travel_date', 'num_adults', 'num_children']
        }),
        ('Contact & Requests', {
            'fields': ['phone', 'special_requests']
        }),
        ('Payment', {
            'fields': ['total_amount']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['user', 'package', 'total_amount']
        return self.readonly_fields


@admin.register(PackageReview)
class PackageReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'package__name', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
