from django.core.management.base import BaseCommand
from django.core.files import File
from packages.models import Company, Package
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Add Northway Tourism company and their packages'

    def handle(self, *args, **kwargs):
        # Create Northway Tourism Company
        company, created = Company.objects.get_or_create(
            slug='northway-tourism',
            defaults={
                'name': 'Northway Tourism',
                'description': 'Experience the beauty of northern Pakistan with Northway Tourism. We offer premium tour packages to the most scenic destinations including Naran, Hunza, Kashmir, and Kalam. Join us for unforgettable journeys through breathtaking landscapes.',
                'email': 'info@northwaytourism.com',
                'phone': '03001234567',
                'website': 'https://www.northwaytourism.com',
                'address': 'Islamabad, Pakistan',
                'rating': 4.75,
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created company: {company.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Company already exists: {company.name}'))

        # Package 1: Naran Babusar Top - 3 Days
        package1, created = Package.objects.get_or_create(
            slug='naran-babusar-top-3-days-northway',
            defaults={
                'company': company,
                'name': 'Naran Babusar Top - 3 Days',
                'description': 'Experience the stunning beauty of Naran Valley and the majestic Babusar Top. This 3-day adventure takes you through picturesque landscapes including Balakot, Kiwai, Naran, Saif-ul-Malook Lake, Bata Kundi, Lulusar Lake, and Babusar Top.',
                'package_type': 'adventure',
                'destination_names': 'Naran, Babusar Top, Balakot, Kiwai, Saif-ul-Malook Lake, Bata Kundi, Lulusar Lake',
                'duration_days': 3,
                'duration_nights': 2,
                'price_per_person': 14800,
                'child_price': 14800,
                'inclusions': '''Transportation from Islamabad (FSD-LHR available)
Hotel accommodation in Naran
Daily breakfast and dinner
Professional tour guide
Visit to Saif-ul-Malook Lake
Visit to Babusar Top
Lulusar Lake stop
All toll taxes and parking charges
Bonfire and outdoor activities''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Jeep charges to Saif-ul-Malook (if required)
Horse riding
Any activities not mentioned in inclusions
Tips for guide and driver''',
                'itinerary': '''Day 1: Departure every Thursday & Monday from Islamabad, drive through Abbottabad and Mansehra, stop at Balakot, continue via Kiwai to Naran, check-in hotel, evening leisure
Day 2: Morning jeep ride to Saif-ul-Malook Lake, exploration and photography, afternoon drive to Bata Kundi, visit Lulusar Lake, reach Babusar Top (weather permitting), return to Naran
Day 3: Optional morning activities, return journey to Islamabad via scenic Kaghan Valley''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package1, 'naltar-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package1.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package1.name}'))

        # Package 2: Hunza Naltar Valley - 5 Days
        package2, created = Package.objects.get_or_create(
            slug='hunza-naltar-valley-5-days-northway',
            defaults={
                'company': company,
                'name': 'Hunza Naltar Valley - 5 Days',
                'description': 'Explore the breathtaking Hunza and Naltar valleys in this comprehensive 5-day tour. Visit Gilgit, Naltar Valley, Hunza Valley, Attabad Lake, and the famous Khunjerab Pass - the highest paved international border crossing in the world.',
                'package_type': 'cultural',
                'destination_names': 'Hunza Valley, Gilgit, Naltar Valley, Besham, Chilas, Babusar Top, Attabad Lake, Khunjerab Pass',
                'duration_days': 5,
                'duration_nights': 4,
                'price_per_person': 22800,
                'child_price': 22800,
                'inclusions': '''Transportation from Islamabad (FSD-LHR available)
Hotel accommodation (double/triple sharing)
Daily breakfast and dinner
Professional tour guide
Visit to Naltar Valley
Visit to Hunza Valley and Karimabad
Attabad Lake visit and boat ride
Khunjerab Pass excursion (weather permitting)
All sightseeing as per itinerary
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Any activities not mentioned in inclusions
Tips for guide and driver
Khunjerab Pass permit charges (if required)''',
                'itinerary': '''Day 1: Departure every Friday from Islamabad, drive via Besham and Chilas to Gilgit, check-in hotel
Day 2: Full day excursion to Naltar Valley, explore the three Naltar lakes, enjoy scenic beauty, return to Gilgit
Day 3: Drive to Hunza Valley via Karakoram Highway, visit Rakaposhi viewpoint, arrival in Karimabad, evening exploration
Day 4: Full day Hunza tour - visit Baltit Fort, Altit Fort, Eagle Nest viewpoint, Attabad Lake, optional trip to Khunjerab Pass
Day 5: Morning leisure, return journey to Islamabad via Karakoram Highway''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package2, 'hunza-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package2.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package2.name}'))

        # Package 3: Kashmir Arang Kel - 3 Days
        package3, created = Package.objects.get_or_create(
            slug='kashmir-arang-kel-3-days-northway',
            defaults={
                'company': company,
                'name': 'Kashmir Arang Kel - 3 Days',
                'description': 'Discover the paradise of Azad Kashmir with this 3-day tour covering Muzaffarabad, Dhani Waterfall, LOC, Kutton Waterfall, Keran, Rattigali (if open), and the stunning Arang Kel village accessible by chairlift.',
                'package_type': 'family',
                'destination_names': 'Kashmir, Muzaffarabad, Arang Kel, Keran, Dhani Waterfall, Kutton Waterfall, LOC, Rattigali',
                'duration_days': 3,
                'duration_nights': 2,
                'price_per_person': 14800,
                'child_price': 14800,
                'inclusions': '''Transportation from Islamabad (FSD-LHR available)
Hotel accommodation in Keran
Daily breakfast and dinner
Professional tour guide
Chairlift ride to Arang Kel
Visit to Dhani Waterfall
Visit to Kutton Waterfall
LOC point visit
Rattigali visit (if open and weather permits)
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Photography charges at certain locations
Any activities not mentioned in inclusions
Tips for guide and driver''',
                'itinerary': '''Day 1: Departure every Thursday & Monday from Islamabad, drive to Muzaffarabad, visit Muzaffarabad city, continue to Keran via Neelum Valley, check-in hotel
Day 2: Morning visit to Dhani Waterfall, drive to LOC and Kutton Waterfall, chairlift to Arang Kel village, exploration and photography, optional visit to Rattigali (if open), return to Keran
Day 3: Morning leisure, drive back to Islamabad via scenic Neelum Valley and Muzaffarabad''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package3, 'swat-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package3.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package3.name}'))

        # Package 4: Kalam Malam Jabba - 3 Days
        package4, created = Package.objects.get_or_create(
            slug='kalam-malam-jabba-3-days-northway',
            defaults={
                'company': company,
                'name': 'Kalam Malam Jabba - 3 Days',
                'description': 'Experience the Switzerland of Pakistan with this 3-day tour of Swat Valley and Kalam. Visit Malam Jabba ski resort, explore Kalam Valley, Ushu Forest, Bahrain, Paloga Valley, and the stunning Mohandand Lake (if open).',
                'package_type': 'family',
                'destination_names': 'Kalam, Swat Valley, Malam Jabba, Bahrain, Ushu Forest, Paloga Valley, Mohandand Lake',
                'duration_days': 3,
                'duration_nights': 2,
                'price_per_person': 14800,
                'child_price': 14800,
                'inclusions': '''Transportation from Islamabad (FSD-LHR available)
Hotel accommodation in Kalam
Daily breakfast and dinner
Professional tour guide
Visit to Malam Jabba ski resort
Kalam Valley exploration
Visit to Ushu Forest
Bahrain stop
Paloga Valley visit
Mohandand Lake visit (if open)
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Skiing equipment rental at Malam Jabba
Chairlift charges at Malam Jabba
Jeep charges to Mohandand Lake
Any activities not mentioned in inclusions
Tips for guide and driver''',
                'itinerary': '''Day 1: Departure every Thursday & Monday from Islamabad, drive through Motorway to Swat, stop at Mingora, visit Malam Jabba ski resort (optional chairlift), continue to Kalam via Bahrain, check-in hotel
Day 2: Full day exploration of Kalam Valley, visit Ushu Forest, Paloga Valley, optional jeep ride to Mohandand Lake (if open and weather permits), fishing in Swat River, photography
Day 3: Morning leisure in Kalam bazaar, optional activities, return journey to Islamabad''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package4, 'kalash-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package4.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package4.name}'))

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Northway Tourism Packages Summary:'))
        self.stdout.write('='*60)
        
        packages_info = [
            (package1, 35800),
            (package2, 55800),
            (package3, 35800),
            (package4, 35800),
        ]
        
        for package, couple_price in packages_info:
            if package:
                self.stdout.write(f'{package.name}')
                self.stdout.write(f'  Solo: PKR {package.price_per_person:,.0f} | Couple: PKR {couple_price:,.0f}')
                self.stdout.write(f'  Duration: {package.duration_days}D/{package.duration_nights}N')
                self.stdout.write(f'  Departure: Every Thursday & Monday' if 'Thursday' in package.itinerary else f'  Departure: Every Friday')
                self.stdout.write('')

        self.stdout.write(self.style.SUCCESS('\n=== All Northway Tourism packages added successfully! ==='))

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
