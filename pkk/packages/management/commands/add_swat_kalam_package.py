from django.core.management.base import BaseCommand
from packages.models import Company, Package
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Add Swat Kalam package to Smile Miles Tour'

    def handle(self, *args, **kwargs):
        # Get Smile Miles Tour Company
        try:
            company = Company.objects.get(slug='smile-miles-tour')
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR('Smile Miles Tour company not found'))
            return

        # Package: Swat Kalam - 3 Days Tour
        package, created = Package.objects.get_or_create(
            slug='swat-kalam-3-days',
            defaults={
                'company': company,
                'name': 'Swat Kalam - 3 Days Tour',
                'description': 'Discover the Switzerland of Pakistan - Swat Valley and Kalam. This 3-day tour takes you through lush green valleys, crystal clear rivers, and majestic mountains. Experience the natural beauty and rich culture of Swat and Kalam.',
                'package_type': 'family',
                'destination_names': 'Swat Valley, Kalam, Malam Jabba, Mingora, Bahrain, Mahodand Lake',
                'duration_days': 3,
                'duration_nights': 2,
                'price_per_person': 15500,
                'child_price': 15500,
                'inclusions': '''Transportation in comfortable vehicle
Hotel accommodation in Kalam (double/triple sharing)
Daily breakfast and dinner
Professional tour guide
Visit to all scenic viewpoints
Malam Jabba chairlift ride (optional)
Visit to Mahodand Lake (seasonal)
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Horse riding at Mahodand Lake
Skiing at Malam Jabba
Any activities not mentioned in inclusions
Tips for guide and driver''',
                'itinerary': '''Day 1: Departure from Islamabad, drive through Motorway to Swat, stop at Takht-e-Bhai Buddhist ruins (optional), visit Mingora city, drive to Kalam via Bahrain, check-in hotel
Day 2: Full day exploration of Kalam, visit Mahodand Lake (seasonal), Ushu Valley, fishing in Swat River, photography at scenic spots, evening walk in Kalam bazaar
Day 3: Morning visit to Malam Jabba ski resort (optional chairlift ride), drive through scenic valleys, return journey to Islamabad''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            # Copy image from destinations to packages
            self.copy_image(package, 'swat-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package.name}'))
            self.stdout.write(f'Package "{package.name}" - Solo: PKR {package.price_per_person}, Couple (2 persons): PKR 38000')
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package.name}'))

        self.stdout.write(self.style.SUCCESS('\n=== Swat Kalam package added successfully! ==='))

    def copy_image(self, package, image_filename):
        """Copy image from media/destinations to package"""
        source_path = os.path.join(settings.MEDIA_ROOT, 'destinations', image_filename)
        
        if os.path.exists(source_path):
            # Create packages directory if it doesn't exist
            packages_dir = os.path.join(settings.MEDIA_ROOT, 'packages')
            os.makedirs(packages_dir, exist_ok=True)
            
            # Copy the image
            dest_filename = f'{package.slug}.jpg'
            dest_path = os.path.join(packages_dir, dest_filename)
            
            # Copy file
            import shutil
            shutil.copy2(source_path, dest_path)
            
            # Update package image field
            package.image = f'packages/{dest_filename}'
            package.save(update_fields=['image'])
            
            self.stdout.write(f'  -> Copied image: {image_filename} to {dest_filename}')
