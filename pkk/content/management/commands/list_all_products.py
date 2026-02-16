from django.core.management.base import BaseCommand
from content.models import Product
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Verify and display all products'

    def handle(self, *args, **kwargs):
        products = Product.objects.all().order_by('name')
        
        self.stdout.write('='*70)
        self.stdout.write(self.style.SUCCESS('ALL PRODUCTS IN DATABASE'))
        self.stdout.write('='*70)
        
        for i, product in enumerate(products, 1):
            self.stdout.write(f'\n{i}. {product.name}')
            self.stdout.write(f'   Price: PKR {product.price}')
            self.stdout.write(f'   Category: {product.category}')
            self.stdout.write(f'   Stock: {product.stock_quantity}')
            self.stdout.write(f'   Image: {product.image.name if product.image else "No image"}')
            self.stdout.write(f'   Available: {"Yes" if product.is_active and product.is_in_stock() else "No"}')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'Total Products: {products.count()}'))
        self.stdout.write('='*70)
        
        # Check for product images in media folder
        media_products_path = os.path.join(settings.MEDIA_ROOT, 'products')
        if os.path.exists(media_products_path):
            media_images = [f for f in os.listdir(media_products_path) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            self.stdout.write(f'\nImages in media/products/: {len(media_images)}')
            for img in media_images:
                self.stdout.write(f'  - {img}')
        
        # Check for product images in static folder
        static_products_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'products')
        if os.path.exists(static_products_path):
            static_images = [f for f in os.listdir(static_products_path) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            self.stdout.write(f'\nImages in static/images/products/: {len(static_images)}')
            for img in static_images:
                self.stdout.write(f'  - {img}')
