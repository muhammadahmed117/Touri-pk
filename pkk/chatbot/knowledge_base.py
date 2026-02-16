"""
TouriPK Website Knowledge Base for AI Chatbot
This file contains comprehensive information about the website features and functionality.
"""

WEBSITE_INFO = {
    "name": "TouriPK (Touri.pk)",
    "tagline": "Discover Pakistan - Your Ultimate Travel Companion",
    "domain": "touri.pk",
    "purpose": "Pakistan's premier tourism platform for discovering destinations, booking packages, and shopping local products",
    "launch_year": 2025
}

# Website Features and Pages
FEATURES = {
    "core_features": [
        "Destination Discovery - Explore 12+ tourist destinations across Northern Pakistan",
        "Trip Cost Calculator - Estimate your travel budget based on destination, people, and days",
        "Tour Packages - Browse pre-made tour packages from verified tour operators",
        "Local Products Store - Shop authentic Pakistani handicrafts, clothing, and souvenirs",
        "Weather Forecast - Check weather conditions for your destination",
        "AI Travel Assistant - 24/7 chatbot support for travel queries",
        "User Dashboard - Manage bookings, wishlist, and travel history",
        "Reviews & Ratings - Read and write destination reviews",
    ],

    "pages": {
        "home": "Homepage with featured destinations and quick links",
        "destinations": "Browse all 12 tourist destinations with filters",
        "destination_detail": "Detailed info about each destination with images, reviews, and tips",
        "packages": "Tour packages from various companies with pricing",
        "products": "Local Pakistani products marketplace",
        "calculator": "Trip cost calculator for budget planning",
        "weather": "Weather forecast checker for destinations",
        "chatbot": "AI travel assistant chat interface",
        "profile": "User profile and dashboard",
        "login": "User login page",
        "register": "New user registration"
    }
}

# Destinations
DESTINATIONS = {
    "total": 12,
    "list": [
        {
            "name": "Neelum Valley",
            "location": "Azad Kashmir",
            "description": "Stunning valley with lush green landscapes, rivers, and mountains",
            "best_time": "May to September",
            "daily_rate": 4500,
            "difficulty": "Moderate",
            "highlights": ["Keran", "Arang Kel", "Ratti Gali Lake", "Sharda"]
        },
        {
            "name": "Hunza Valley",
            "location": "Gilgit-Baltistan",
            "description": "Famous for Karimabad, Baltit Fort, and stunning mountain views",
            "best_time": "April to October",
            "daily_rate": 6000,
            "difficulty": "Easy to Moderate",
            "highlights": ["Baltit Fort", "Altit Fort", "Attabad Lake", "Eagles Nest"]
        },
        {
            "name": "Skardu",
            "location": "Gilgit-Baltistan",
            "description": "Gateway to K2, famous for lakes and mountain ranges",
            "best_time": "April to October",
            "daily_rate": 5000,
            "difficulty": "Moderate",
            "highlights": ["Shangrila Resort", "Satpara Lake", "Deosai Plains", "Shigar Fort"]
        },
        {
            "name": "Fairy Meadows",
            "location": "Gilgit-Baltistan",
            "description": "Base camp for Nanga Parbat, breathtaking mountain views",
            "best_time": "May to September",
            "daily_rate": 5500,
            "difficulty": "Hard",
            "highlights": ["Nanga Parbat View", "Beyal Camp", "Raikot Glacier"]
        },
        {
            "name": "Deosai Plains",
            "location": "Gilgit-Baltistan",
            "description": "Second-highest plateau in the world, famous for wildlife",
            "best_time": "June to September",
            "daily_rate": 5800,
            "difficulty": "Moderate",
            "highlights": ["Sheosar Lake", "Brown Bears", "Wildflowers", "Bara Pani"]
        },
        {
            "name": "Naran & Kaghan",
            "location": "Khyber Pakhtunkhwa",
            "description": "Popular hill stations with lakes and valleys",
            "best_time": "May to September",
            "daily_rate": 4800,
            "difficulty": "Easy",
            "highlights": ["Saif-ul-Malook Lake", "Babusar Pass", "Lulusar Lake", "Ansoo Lake"]
        },
        {
            "name": "K2 Base Camp",
            "location": "Gilgit-Baltistan",
            "description": "Trekking to the world's second-highest mountain",
            "best_time": "June to August",
            "daily_rate": 7000,
            "difficulty": "Very Hard",
            "highlights": ["K2 View", "Concordia", "Baltoro Glacier", "Gondogoro La"]
        },
        {
            "name": "Swat Valley",
            "location": "Khyber Pakhtunkhwa",
            "description": "Switzerland of Pakistan with lush landscapes",
            "best_time": "April to October",
            "daily_rate": 4200,
            "difficulty": "Easy",
            "highlights": ["Malam Jabba", "Kalam", "Mahodand Lake", "Fizagat"]
        },
        {
            "name": "Murree",
            "location": "Punjab",
            "description": "Popular hill station near Islamabad",
            "best_time": "Year-round",
            "daily_rate": 3800,
            "difficulty": "Easy",
            "highlights": ["Mall Road", "Patriata", "Kashmir Point", "Pindi Point"]
        },
        {
            "name": "Naltar Valley",
            "location": "Gilgit-Baltistan",
            "description": "Famous for colorful lakes and ski resort",
            "best_time": "April to October",
            "daily_rate": 5500,
            "difficulty": "Moderate",
            "highlights": ["Naltar Lakes", "Ski Resort", "Pine Forests"]
        },
        {
            "name": "Chitral",
            "location": "Khyber Pakhtunkhwa",
            "description": "Remote valley with unique Kalash culture",
            "best_time": "May to September",
            "daily_rate": 4000,
            "difficulty": "Moderate",
            "highlights": ["Kalash Valleys", "Chitral Fort", "Tirich Mir", "Shandur Pass"]
        },
        {
            "name": "Baltit Fort",
            "location": "Hunza, Gilgit-Baltistan",
            "description": "Ancient fort with panoramic valley views",
            "best_time": "April to October",
            "daily_rate": 5200,
            "difficulty": "Easy",
            "highlights": ["Historical Fort", "Karimabad", "Mountain Views"]
        }
    ]
}

# Cost Calculator Information
CALCULATOR_INFO = {
    "url": "/content/calculator/",
    "description": "Estimate your trip cost based on destination, number of people, and days",
    "how_it_works": "Select a destination, enter number of travelers and days, get instant cost estimate",
    "formula": {
        "total": "Accommodation + Transportation + Activities",
        "accommodation": "Daily Rate × People × Days",
        "transportation": "8,000 + (1,000 × People)",
        "activities": "3,000 × People"
    },
    "pricing_range": {
        "budget": "Rs. 15,000 - 35,000 for 2 people, 2-3 days",
        "standard": "Rs. 35,000 - 80,000 for 2 people, 3-5 days",
        "premium": "Rs. 80,000+ for longer trips or remote destinations"
    }
}

# Packages Information
PACKAGES_INFO = {
    "url": "/packages/",
    "description": "Pre-made tour packages from verified tour operators",
    "types": [
        "Family Tours",
        "Adventure Tours",
        "Honeymoon Packages",
        "Group Tours",
        "Luxury Tours",
        "Budget Tours",
        "Cultural Tours",
        "Religious Tours"
    ],
    "features": [
        "All-inclusive pricing",
        "Transportation included",
        "Hotel bookings",
        "Guided tours",
        "Meal plans",
        "Activity packages"
    ]
}

# Products Information
PRODUCTS_INFO = {
    "url": "/content/products/",
    "description": "Authentic Pakistani handicrafts and souvenirs",
    "categories": [
        "Handicrafts - Traditional crafts and pottery",
        "Clothing - Traditional dresses, shawls, and embroidered items",
        "Food & Beverages - Local spices, honey, dry fruits",
        "Books & Media - Travel guides and cultural books",
        "Accessories - Jewelry, bags, and decorative items"
    ]
}

# User Features
USER_FEATURES = {
    "registration": "Create account with email, username, and password",
    "login": "Secure login system",
    "dashboard": "View bookings, saved destinations, and travel history",
    "wishlist": "Save favorite destinations for later",
    "reviews": "Write reviews and ratings for destinations",
    "profile_management": "Update personal information and preferences"
}

# Weather Feature
WEATHER_INFO = {
    "url": "/content/check-weather/",
    "description": "Check current weather and forecast for any Pakistani city",
    "how_to_use": "Enter city name and get real-time weather data"
}

# Booking Process
BOOKING_PROCESS = {
    "steps": [
        "1. Browse destinations or packages",
        "2. Check details, pricing, and reviews",
        "3. Use cost calculator to estimate budget",
        "4. Login or create account",
        "5. Select package or contact tour operator",
        "6. Make booking and payment",
        "7. Receive confirmation via email",
        "8. Enjoy your trip!"
    ]
}

# Travel Tips
TRAVEL_TIPS = [
    "Book accommodations 2-3 weeks in advance for better rates",
    "Visit during off-season (October-March) for 20-30% lower prices",
    "Carry local currency (PKR) as cards aren't widely accepted in remote areas",
    "Pack warm clothing even in summer for high-altitude destinations",
    "Hire local guides for authentic experiences and better pricing",
    "Always keep emergency funds (10-15% extra budget)",
    "Check weather forecasts before traveling",
    "Respect local culture and traditions",
    "Stay hydrated at high altitudes",
    "Purchase travel insurance for adventure activities"
]

# Best Times to Visit
SEASONAL_INFO = {
    "spring": {
        "months": "March to May",
        "best_for": ["Hunza", "Skardu", "Swat Valley"],
        "highlights": "Blooming flowers, pleasant weather",
        "crowd_level": "Moderate"
    },
    "summer": {
        "months": "June to August",
        "best_for": ["Fairy Meadows", "Deosai Plains", "Naran & Kaghan"],
        "highlights": "Peak season, all areas accessible",
        "crowd_level": "High"
    },
    "autumn": {
        "months": "September to November",
        "best_for": ["Hunza", "Chitral", "Skardu"],
        "highlights": "Golden foliage, fewer tourists, lower prices",
        "crowd_level": "Low to Moderate"
    },
    "winter": {
        "months": "December to February",
        "best_for": ["Murree", "Malam Jabba"],
        "highlights": "Snow activities, lowest prices",
        "crowd_level": "Low (many areas closed)"
    }
}

# FAQs
COMMON_QUESTIONS = {
    "how_to_book": "Browse destinations/packages, select one, login, and follow booking process",
    "payment_methods": "Credit/debit cards, bank transfers, and cash on some packages",
    "cancellation_policy": "Varies by tour operator, check specific package details",
    "group_discounts": "Yes, larger groups (5+ people) often get discounted rates",
    "custom_packages": "Contact tour operators directly for customized itineraries",
    "safety": "All listed tour operators are verified; follow standard travel safety guidelines",
    "required_documents": "CNIC for domestic travelers, passport for international visitors",
    "accommodation_types": "Hotels, guest houses, camping options available",
    "transportation": "Packages include transportation; individual travelers can hire local transport"
}

# Website Navigation
NAVIGATION = {
    "main_menu": [
        "Home - Featured destinations and quick access",
        "Destinations - Browse all tourist spots",
        "Packages - Tour packages from operators",
        "Products - Local handicrafts store",
        "Calculator - Trip cost estimator",
        "Weather - Weather forecast tool",
        "Chatbot - AI travel assistant (you are here!)"
    ],
    "user_menu": [
        "Dashboard - Your bookings and activity",
        "Profile - Manage account settings",
        "Wishlist - Saved destinations",
        "Logout - Sign out of account"
    ]
}

# Contact and Support
SUPPORT_INFO = {
    "chatbot": "24/7 AI assistant for instant help (this chat)",
    "email": "Available through contact forms",
    "working_hours": "Chatbot: 24/7, Human support: 9 AM - 6 PM PKT"
}

