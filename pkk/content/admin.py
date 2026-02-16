from django.contrib import admin
from .models import Destination, Product, CustomPackageOrder, AdminNotification

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'price', 'category', 'is_approved', 'is_active', 'created_at')
    list_filter = ('is_approved', 'is_active', 'category', 'company')
    search_fields = ('name', 'description')
    ordering = ('created_at',)  # FIFO queue: oldest first
    actions = ['approve_products']
    
    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} products approved.')
    approve_products.short_description = 'Approve selected products'

# CustomPackageOrder and AdminNotification removed from admin portal