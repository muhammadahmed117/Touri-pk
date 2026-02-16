from django.core.management.base import BaseCommand
from content.models import Product

class Command(BaseCommand):
    help = 'Add initial products from media/products folder'

    def handle(self, *args, **kwargs):
        products_data = [
            {
                'name': 'Premium Almonds',
                'description': 'Fresh, crunchy almonds from the valleys of Gilgit-Baltistan. Rich in nutrients and perfect for snacking or cooking. These premium quality almonds are carefully selected and packed to maintain their natural flavor and nutritional value.',
                'price': 1500.00,
                'image': 'products/Almond.jpg',
                'category': 'food',
                'stock_quantity': 50,
                'is_featured': True,
                'is_active': True,
            },
            {
                'name': 'Dried Apricots',
                'description': 'Sweet and tangy dried apricots from Hunza Valley. Known for their exceptional taste and health benefits, these sun-dried apricots are a natural source of vitamins and minerals. Perfect for healthy snacking.',
                'price': 1200.00,
                'image': 'products/dried-apricots.jpg',
                'category': 'food',
                'stock_quantity': 75,
                'is_featured': True,
                'is_active': True,
            },
            {
                'name': 'Pure Shilajit',
                'description': 'Authentic Himalayan Shilajit from the mountains of Gilgit-Baltistan. This rare mineral pitch is known for its incredible health benefits and is used in traditional medicine. 100% pure and lab-tested for quality.',
                'price': 3500.00,
                'image': 'products/Shilajit.jpg',
                'category': 'food',
                'stock_quantity': 30,
                'is_featured': True,
                'is_active': True,
            },
            {
                'name': 'Premium Walnuts',
                'description': 'High-quality walnuts sourced from the lush valleys of northern Pakistan. These walnuts are rich in omega-3 fatty acids and antioxidants. Perfect for baking, cooking, or enjoying as a nutritious snack.',
                'price': 1800.00,
                'image': 'products/Walnuts.jpg',
                'category': 'food',
                'stock_quantity': 60,
                'is_featured': False,
                'is_active': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for product_data in products_data:
            product, created = Product.objects.update_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated product: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} products created, {updated_count} products updated'
            )
        )
