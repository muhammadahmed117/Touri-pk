from django.core.management.base import BaseCommand
from django.core.files import File
from packages.models import Company, Package
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Add Smile Miles Tour company and their packages'

    def handle(self, *args, **kwargs):
        # Create Smile Miles Tour Company
        company, created = Company.objects.get_or_create(
            slug='smile-miles-tour',
            defaults={
                'name': 'Smile Miles Tour',
                'description': 'Built for Life like a Dream. Join us for an unforgettable experience filled with adventure, culture and excitement. A journey to the Foot of Nanga Parbat.',
                'email': 'info@smile4milestour.com',
                'phone': '03067004848',
                'website': 'https://www.smile4milestour.com',
                'address': 'Pakistan',
                'rating': 4.80,
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created company: {company.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Company already exists: {company.name}'))

        # Package 1: Fairy Meadows - 5 Days Tour
        package1, created = Package.objects.get_or_create(
            slug='fairy-meadows-5-days',
            defaults={
                'company': company,
                'name': 'Fairy Meadows - 5 Days Tour',
                'description': 'Experience the breathtaking beauty of Fairy Meadows with stunning views of Nanga Parbat, the ninth highest mountain in the world. This 5-day adventure takes you through lush green meadows, pristine landscapes, and offers an unforgettable camping experience.',
                'package_type': 'adventure',
                'destination_names': 'Fairy Meadows, Nanga Parbat, Raikot Bridge, Tato Village',
                'duration_days': 5,
                'duration_nights': 4,
                'price_per_person': 25000,
                'child_price': 25000,
                'inclusions': '''Transportation from pickup point to Fairy Meadows and back
Accommodation in camping tents
All meals (Breakfast, Lunch, Dinner)
Professional tour guide
Jeep ride from Raikot Bridge to Tato Village
Porter services for luggage
First aid kit and emergency support
All permits and entry fees''',
                'exclusions': '''Personal expenses and shopping
Travel insurance
Any meals not mentioned in inclusions
Tips for guides and porters
Emergency evacuation costs''',
                'itinerary': '''Day 1: Departure from Islamabad/Rawalpindi, drive to Raikot Bridge, jeep ride to Tato Village, trek to Fairy Meadows basecamp
Day 2: Explore Fairy Meadows, optional trek to Nanga Parbat viewpoint, photography and nature walks
Day 3: Trek to Beyal Camp for closer views of Nanga Parbat, camping and stargazing
Day 4: Return trek from Beyal Camp to Fairy Meadows, leisure time and bonfire
Day 5: Trek back to Tato Village, jeep ride to Raikot Bridge, return journey to Islamabad''',
                'min_people': 1,
                'max_people': 15,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            # Copy image from destinations to packages
            self.copy_image(package1, 'fairy-meadows.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package1.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package1.name}'))

        # Package 2: Hunza Valley - 5 Days Tour
        package2, created = Package.objects.get_or_create(
            slug='hunza-valley-5-days',
            defaults={
                'company': company,
                'name': 'Hunza Valley - 5 Days Tour',
                'description': 'Discover the enchanting Hunza Valley, known for its majestic mountains, ancient forts, and warm hospitality. This 5-day tour covers the most beautiful spots in Hunza including Karimabad, Baltit Fort, and stunning viewpoints.',
                'package_type': 'cultural',
                'destination_names': 'Hunza Valley, Karimabad, Baltit Fort, Altit Fort, Attabad Lake, Eagle Nest',
                'duration_days': 5,
                'duration_nights': 4,
                'price_per_person': 25000,
                'child_price': 25000,
                'inclusions': '''Transportation in comfortable vehicle
Hotel accommodation (double/triple sharing)
Daily breakfast and dinner
Professional tour guide
All sightseeing as per itinerary
Visit to Baltit Fort and Altit Fort
Eagle Nest viewpoint visit
Attabad Lake boat ride
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Any activities not mentioned in inclusions
Tips for guide and driver''',
                'itinerary': '''Day 1: Departure from Islamabad, drive through Karakoram Highway, stop at Rakaposhi viewpoint, arrival in Hunza
Day 2: Full day tour of Karimabad, visit Baltit Fort, Altit Fort, explore local bazaar, sunset at Eagle Nest viewpoint
Day 3: Day trip to Attabad Lake, boat ride, visit Gulmit and Passu Cones, photography session
Day 4: Visit to Khunjerab Pass (subject to weather), highest paved border crossing in the world, return to Hunza
Day 5: Morning leisure, optional visit to local market, return journey to Islamabad''',
                'min_people': 1,
                'max_people': 15,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package2, 'hunza-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package2.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package2.name}'))

        # Package 3: Naran Valley - 3 Days Tour
        package3, created = Package.objects.get_or_create(
            slug='naran-valley-3-days',
            defaults={
                'company': company,
                'name': 'Naran Valley - 3 Days Tour',
                'description': 'Experience the natural beauty of Naran Valley with its crystal clear lakes, lush green valleys, and thrilling activities. This 3-day adventure includes visits to Saif-ul-Malook Lake, river rafting, and scenic landscapes.',
                'package_type': 'adventure',
                'destination_names': 'Naran, Kaghan Valley, Saif-ul-Malook Lake, Shogran, Siri Paye',
                'duration_days': 3,
                'duration_nights': 2,
                'price_per_person': 16000,
                'child_price': 16000,
                'inclusions': '''Transportation in comfortable vehicle
Hotel accommodation in Naran
Daily breakfast and dinner
Professional tour guide
Visit to Saif-ul-Malook Lake
River rafting experience (seasonal)
Jeep ride to lake
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Horse riding at Saif-ul-Malook
Any activities not mentioned in inclusions
Tips for guide and driver''',
                'itinerary': '''Day 1: Departure from Islamabad, drive through scenic Kaghan Valley, stops at Balakot and Shogran, arrival in Naran, evening walk
Day 2: Early morning trip to Saif-ul-Malook Lake by jeep, photography and exploration, return to Naran, river rafting in Kunhar River (seasonal), evening leisure
Day 3: Optional morning visit to Lalazar or local market, return journey to Islamabad via Abbottabad''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package3, 'naltar-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package3.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package3.name}'))

        # Package 4: Neelum Valley - 3 Days Tour
        package4, created = Package.objects.get_or_create(
            slug='neelum-valley-3-days',
            defaults={
                'company': company,
                'name': 'Neelum Valley - 3 Days Tour',
                'description': 'Explore the pristine beauty of Neelum Valley in Azad Kashmir, known for its lush green forests, crystal clear rivers, and charming villages. This 3-day tour takes you through the most scenic spots of this paradise on earth.',
                'package_type': 'family',
                'destination_names': 'Neelum Valley, Muzaffarabad, Keran, Sharda, Kel, Arang Kel',
                'duration_days': 3,
                'duration_nights': 2,
                'price_per_person': 15500,
                'child_price': 15500,
                'inclusions': '''Transportation in comfortable vehicle
Hotel accommodation (double/triple sharing)
Daily breakfast and dinner
Professional tour guide
All sightseeing as per itinerary
Chair lift ride to Arang Kel
Visit to Sharda University ruins
All toll taxes and parking charges''',
                'exclusions': '''Lunch during the tour
Personal expenses and shopping
Travel insurance
Any activities not mentioned in inclusions
Tips for guide and driver
Photography charges at certain locations''',
                'itinerary': '''Day 1: Departure from Islamabad, drive to Muzaffarabad, continue along Neelum River to Keran, check-in hotel, evening riverside walk
Day 2: Drive to Sharda, visit Sharda University ruins and Sharda Peak viewpoint, continue to Kel, chair lift to Arang Kel village, return to Keran
Day 3: Morning leisure at Keran, optional visit to local bazaar, return journey to Islamabad via Muzaffarabad''',
                'min_people': 2,
                'max_people': 20,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.copy_image(package4, 'swat-valley.jpg')
            self.stdout.write(self.style.SUCCESS(f'Created package: {package4.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Package already exists: {package4.name}'))

        # Update couple prices (these are double the solo prices as shown in the image)
        packages_to_update = [
            (package1, 50000),
            (package2, 60000),
            (package3, 40000),
            (package4, 38000),
        ]
        
        for package, couple_price in packages_to_update:
            if package:
                # Note: In the model we store per-person price, the couple price shown is total for 2 people
                self.stdout.write(f'Package "{package.name}" - Solo: PKR {package.price_per_person}, Couple (2 persons): PKR {couple_price}')

        self.stdout.write(self.style.SUCCESS('\n=== All Smile Miles Tour packages added successfully! ==='))

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
