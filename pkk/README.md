# TouriPK - Pakistan Tourism Platform

A comprehensive Django-based tourism platform for exploring and booking tours in Pakistan.

## Features

- **Destinations**: Browse beautiful destinations across Pakistan
- **Tour Packages**: View and book tour packages from verified operators
- **Products**: Shop for local products and souvenirs
- **Custom Package Calculator**: Calculate custom tour package costs
- **Weather Information**: Check weather for your destinations
- **AI Chatbot**: Get travel assistance and recommendations
- **Shopping Cart**: Purchase products with secure checkout
- **Company Portal**: Tour operators can register and manage packages

## Prerequisites

- Python 3.12+
- pip (Python package manager)

## Installation Steps

1. Clone or download this repository

2. Navigate to the project directory

3. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update settings as needed (SECRET_KEY, DEBUG, etc.)

6. Initialize the database:
```bash
python manage.py migrate
```

7. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

8. **Configure AI Chatbot** (Optional):
   - Get a DeepSeek API key from https://platform.deepseek.com/
   - Edit `chatbot/config.py` and add your API key

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application:
   - Main website: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

- `content/` - Destinations, products, cost calculator, weather
- `packages/` - Tour packages and company management
- `users/` - User authentication and profiles
- `chatbot/` - AI travel assistant
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, images
- `media/` - User uploaded files

## Technologies Used

- Django 5.1.13
- Bootstrap 5.3.0
- Font Awesome 6.0.0
- Python 3.12+

## License

All rights reserved.

## Contact

For support or inquiries, visit TouriPK.
- Cost Calculator for Trip Planning
- Weather Information
- Admin Interface for Content Management
- Enhanced Modern UI with Animations

## Default Sample Data

The application comes with sample data including:
- 3 tourist destinations (Hunza Valley, Skardu, Swat Valley)
- 3 local products (Dried Apricots, Traditional Shawl, Handicraft Box)

## Notes

- This is a prototype version for demonstration purposes
- Uses placeholder images for destinations and products
- All passwords are handled securely with Django's authentication system