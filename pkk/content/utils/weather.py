import requests
from datetime import datetime
from django.core.cache import cache
from django.conf import settings

# WeatherAPI.com configuration
API_KEY = getattr(settings, 'WEATHERAPI_KEY', '51669905e0fc4974b5b131221251012')
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

# Pakistan cities mapping for accurate results
PAKISTAN_CITIES = {
    'naran': 'Naran, Pakistan',
    'murree': 'Murree, Pakistan',
    'gilgit': 'Gilgit, Pakistan',
    'skardu': 'Skardu, Pakistan',
    'hunza': 'Hunza, Pakistan',
    'swat': 'Swat, Pakistan',
    'chitral': 'Chitral, Pakistan',
    'kaghan': 'Kaghan, Pakistan',
    'islamabad': 'Islamabad, Pakistan',
    'lahore': 'Lahore, Pakistan',
    'karachi': 'Karachi, Pakistan',
    'peshawar': 'Peshawar, Pakistan',
    'quetta': 'Quetta, Pakistan',
    'faisalabad': 'Faisalabad, Pakistan',
    'multan': 'Multan, Pakistan',
    'rawalpindi': 'Rawalpindi, Pakistan',
}

def get_weather_data(city):
    # Normalize city name for consistent caching
    city_normalized = city.strip().lower()
    
    # Use Pakistan-specific location if available
    api_query = PAKISTAN_CITIES.get(city_normalized, f"{city}, Pakistan")
    
    # Check cache first
    cache_key = f'weather_{city_normalized}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    # Make API request if not in cache
    params = {
        'key': API_KEY,
        'q': api_query,
        'aqi': 'no'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'temperature': round(data['current']['temp_c'], 1),
                'feels_like': round(data['current']['feelslike_c'], 1),
                'humidity': data['current']['humidity'],
                'description': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'wind_speed': round(data['current']['wind_kph'] / 3.6, 1),  # Convert kph to m/s
                'last_updated': data['current']['last_updated'],
                'city_name': data['location']['name'],  # Get the actual city name from API
                'country': data['location']['country'],
                'region': data['location'].get('region', '')
            }
            # Cache for 15 minutes (shorter for more accurate data)
            cache.set(cache_key, weather_info, timeout=900)
            return weather_info
        else:
            print(f"Weather API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None