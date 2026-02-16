<p align="center">
  <img src="static/images/logo.png" alt="TouriPK Logo" width="200"/>
</p>

<h1 align="center">🇵🇰 TouriPK — Pakistan Tourism Platform</h1>

<p align="center">
  <strong>A comprehensive Django-based tourism platform for exploring, booking, and experiencing the beauty of Pakistan.</strong>
</p>

<p align="center">
  <a href="https://rohaannoor123.pythonanywhere.com">🌐 Live Demo</a> •
  <a href="#features">✨ Features</a> •
  <a href="#installation">⚙️ Installation</a> •
  <a href="#usage">📖 Usage</a> •
  <a href="#project-structure">📁 Structure</a>
</p>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 About

**TouriPK** (Touri.pk) is a full-stack tourism web application built with Django that serves as a one-stop platform for travelers visiting Pakistan. It connects tourists with tour operators, provides destination guides with real-time weather, offers a product marketplace for local goods, and includes an AI-powered travel chatbot for personalized assistance.

The platform supports **two user roles**:
- **Tourists** — Browse destinations, book packages, shop products, use the trip calculator, and get AI chatbot help
- **Tour Companies** — Register with CNIC verification, manage packages & products, handle bookings, and respond to support tickets

---

## ✨ Features

### 🏔️ Destination Guides
- Browse curated destinations across Pakistan with rich descriptions, image galleries, and difficulty levels
- Filter by tags, search by name, and view featured destinations
- User reviews with verified badges and helpful vote system
- Travel tips contributed by the community
- SEO-optimized meta titles and descriptions

### 📦 Tour Packages
- Browse packages by type: Family, Adventure, Honeymoon, Group, Luxury, Budget, Cultural, Religious
- Detailed itineraries with inclusions/exclusions
- View count tracking and average star ratings
- Filter by company, package type, and price range
- Package reviews from verified travelers (post-completion only)

### 🛒 Product Marketplace
- Shop local products: Clothing, Food, Handicrafts, Books, Accessories
- Weight-based shipping calculation (≤2kg = PKR 200, +PKR 50 per extra kg)
- Full shopping cart with AJAX add/update/remove
- Order management with status tracking (Pending → Confirmed → Processing → Shipped → Delivered)
- Verified-purchase product reviews
- Company product listings with admin approval workflow

### 🧮 Trip Cost Calculator
- Interactive calculator with per-destination cost components
- Categories: Camping, Transport, Food, Activities, Shopping, Miscellaneous
- Advanced breakdown with customizable quantities
- Custom package builder with dynamic pricing (destination, duration, people, vehicle, food, accommodation, guide, bonfire)
- Instant per-person cost calculation

### 🤖 AI Travel Chatbot
- Powered by DeepSeek API with context-aware travel knowledge
- Floating widget accessible on every page (authenticated users)
- Conversation history with session management
- Intelligent filtering of non-travel-related questions
- Real-time responses via AJAX

### 🌤️ Weather Forecasting
- Real-time weather data for Pakistani cities via WeatherAPI.com
- Temperature, conditions, humidity, and wind information
- Response caching for performance

### 💳 Payment Integration
- **Stripe** integration for secure online payments (packages & custom orders)
- **Bank Transfer** option with transaction ID validation
- **Cash on Delivery (COD)** for product orders
- Payment intent creation and confirmation flow
- Admin notifications for new orders and payments

### 🏢 Company Portal
- Company registration with CNIC front/back upload
- Admin approval workflow (Pending → Approved → Rejected)
- Full CRUD for tour packages and products
- Booking management with status updates
- Company dashboard with stats and analytics

### 🎫 Support Ticket System
- Create tickets linked to specific orders, packages, or companies
- Issue types: Delivery, Quality, Package, Billing, Booking, Refund, General
- Priority levels: Low, Medium, High, Urgent
- **48-hour auto-escalation SLA** for unresolved tickets
- Threaded conversations between customer, company, and admin
- Admin escalation panel

### 👤 User Management
- Email-based authentication (email as username)
- Separate registration flows for tourists and companies
- User profiles with travel preferences and emergency contacts
- Dashboard with booking history and stats
- User follow system and wishlists
- Notification system (booking, review, follow, message, system)
- Rate-limited login (10/5min) and registration (15/hr)

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Django 5.1+, Python 3.10+ |
| **Frontend** | Tailwind CSS, Bootstrap 5.3, Font Awesome 6 |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **API** | Django REST Framework, SimpleJWT |
| **Real-time** | Django Channels (WebSockets) |
| **Payments** | Stripe |
| **AI Chatbot** | DeepSeek API |
| **Weather** | WeatherAPI.com |
| **Auth** | Django built-in auth |
| **Security** | Argon2 password hashing, django-ratelimit, CSRF |
| **Other** | django-taggit, django-filter, django-cors-headers, WhiteNoise |

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/muhammadahmed117/Touri-pk.git
cd Touri-pk
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe (for payments)
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# DeepSeek AI (for chatbot)
DEEPSEEK_API_KEY=your-deepseek-api-key

# Weather API
WEATHER_API_KEY=your-weatherapi-key
```

### Step 5: Database Setup

```bash
python manage.py migrate
```

### Step 6: Load Sample Data (Optional)

```bash
python manage.py loaddata content/fixtures/initial_data.json
python manage.py loaddata content/fixtures/destination_costs.json
```

### Step 7: Create Admin Account

```bash
python manage.py createsuperuser
```

### Step 8: Run the Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## 🔧 Configuration

### Stripe Payments
1. Create a [Stripe account](https://stripe.com)
2. Get your API keys from the Stripe Dashboard
3. Add `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` to `.env`

### AI Chatbot (DeepSeek)
1. Get an API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. Add `DEEPSEEK_API_KEY` to `.env`
3. The chatbot configuration is in `chatbot/config.py`

### Weather API
1. Get a free API key from [WeatherAPI.com](https://www.weatherapi.com/)
2. Add `WEATHER_API_KEY` to `.env`

---

## 📖 Usage

### For Tourists
1. **Register** as a Tourist user
2. **Browse** destinations, packages, and products
3. **Book** a tour package or create a custom package
4. **Shop** local products with cart and checkout
5. **Use** the AI chatbot for travel recommendations
6. **Check** weather for your destination
7. **Calculate** trip costs with the interactive calculator
8. **Submit** support tickets if you need help

### For Tour Companies
1. **Register** as a Company with CNIC verification documents
2. **Wait** for admin approval
3. **Access** the Company Portal dashboard
4. **Add** tour packages with itineraries and pricing
5. **List** local products for sale
6. **Manage** bookings and update statuses
7. **Respond** to customer support tickets

### For Admins
1. Access `/admin/` for the Django admin panel
2. Approve/reject company registrations
3. Manage all content, users, and orders
4. View escalated support tickets
5. Monitor admin notifications for new orders

---

## 📁 Project Structure

```
Touri-pk/
│
├── touripk/                    # Project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point (Channels)
│
├── content/                    # Destinations, Products, Orders
│   ├── models.py               # Destination, Product, Cart, Order, Review, etc.
│   ├── views.py                # 20+ views (home, shop, calculator, payments)
│   ├── admin.py                # Admin registrations
│   ├── urls.py                 # Content URL patterns
│   ├── fixtures/               # Sample data (destinations, costs)
│   └── utils/
│       └── weather.py          # WeatherAPI integration
│
├── packages/                   # Tour Packages & Bookings
│   ├── models.py               # Company, Package, Booking, PackageReview
│   ├── views.py                # Package listing, booking, payments
│   ├── company_views.py        # Company portal (CRUD packages/products)
│   ├── company_forms.py        # Company-specific forms
│   └── urls.py                 # Package URL patterns
│
├── users/                      # Authentication & User Profiles
│   ├── models.py               # CustomUser, UserProfile, Notification
│   ├── views.py                # Register, Login, Dashboard
│   ├── forms.py                # Registration & login forms
│   └── urls.py                 # User URL patterns
│
├── chatbot/                    # AI Travel Assistant
│   ├── models.py               # ChatSession, ChatMessage
│   ├── views.py                # Chat API endpoints
│   ├── config.py               # DeepSeek API configuration
│   ├── knowledge_base.py       # Travel knowledge context
│   └── prompt_builder.py       # AI prompt construction
│
├── support/                    # Customer Support System
│   ├── models.py               # SupportTicket, TicketMessage
│   ├── views.py                # Ticket CRUD, escalation, admin panel
│   ├── forms.py                # Ticket creation forms
│   └── urls.py                 # Support URL patterns
│
├── templates/                  # HTML Templates
│   ├── base.html               # Base template (navbar, footer, chatbot widget)
│   ├── content/                # Destination, product, cart, order templates
│   ├── packages/               # Package, booking, company templates
│   ├── users/                  # Login, register, dashboard templates
│   ├── chatbot/                # Chat widget template
│   └── support/                # Ticket templates
│
├── static/                     # Static assets (CSS, images)
├── media/                      # User-uploaded files (gitignored)
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── .env                        # Environment variables (not committed)
```

---

## 🔌 API Endpoints

### Content & Shopping
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage with featured content |
| GET | `/content/destinations/` | Destination listing with search & filters |
| GET | `/content/destinations/<id>/` | Destination detail page |
| GET | `/content/products/` | Product listing by category |
| GET | `/content/weather/` | Weather checker for Pakistani cities |
| GET | `/content/calculator/` | Trip cost calculator |
| POST | `/content/add-to-cart/<id>/` | Add product to cart (AJAX) |
| GET | `/content/cart/` | View shopping cart |
| POST | `/content/checkout/` | Checkout page |
| POST | `/content/custom-package/` | Custom package builder |
| POST | `/content/create-payment-intent/` | Stripe payment intent |

### Packages & Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/packages/` | Package listing with filters |
| GET | `/packages/<slug>/` | Package detail page |
| GET | `/packages/company/<slug>/` | Company profile |
| POST | `/packages/<slug>/book/` | Create booking |
| GET | `/packages/my-bookings/` | User's bookings |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/users/register/` | Tourist registration |
| GET/POST | `/users/register/company/` | Company registration |
| GET/POST | `/users/login/` | User login |
| GET | `/users/dashboard/` | User dashboard |

### Support
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/support/create/` | Create support ticket |
| GET | `/support/my-tickets/` | Customer's tickets |
| GET | `/support/ticket/<id>/` | Ticket detail & conversation |
| POST | `/support/ticket/<id>/resolve/` | Resolve ticket |
| POST | `/support/ticket/<id>/escalate/` | Escalate ticket |

### Chatbot
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chatbot/send/` | Send message to AI chatbot |
| GET | `/chatbot/history/` | Get chat history |

---

## 🗄️ Database Models

### Content App (14 models)
- **Destination** — Tourist destinations with images, difficulty levels, tags, and SEO metadata
- **DestinationImage** — Gallery images for destinations
- **Product** — Marketplace products with categories, stock, weight, and company association
- **CostComponent** — Cost breakdown items per destination for the trip calculator
- **Review / ProductReview** — User reviews with 1-5 star ratings and verification
- **Wishlist** — Saved/bookmarked destinations
- **TravelTip** — Community-contributed travel tips
- **Cart / CartItem** — Shopping cart with weight-based shipping fees
- **Order / OrderItem** — E-commerce orders with full status lifecycle
- **CustomPackageOrder** — Custom tour packages with Stripe payment integration
- **AdminNotification** — Backend alerts for orders, payments, and custom packages

### Packages App (4 models)
- **Company** — Tour operators with CNIC verification and admin approval workflow
- **Package** — Tour packages with itineraries, pricing tiers, and 8 package types
- **Booking** — Reservations with payment tracking and status management
- **PackageReview** — Verified post-completion reviews

### Users App (3 models)
- **CustomUser** — Extended user model with dual roles (tourist/company), email-based auth
- **UserProfile** — Travel preferences, budget range, and emergency contacts
- **Notification** — In-app notification system (booking, review, follow, message, system)

### Support App (2 models)
- **SupportTicket** — Tickets with priority levels and 48-hour auto-escalation SLA
- **TicketMessage** — Threaded conversation messages between customer, company, and admin

### Chatbot App (2 models)
- **ChatSession** — Chat conversation sessions per user
- **ChatMessage** — Individual messages with AI responses

---

## 🚀 Deployment

### PythonAnywhere (Current)

The application is deployed at **[rohaannoor123.pythonanywhere.com](https://rohaannoor123.pythonanywhere.com)**

Key deployment settings:
- Python 3.10 with virtualenv
- SQLite database
- WhiteNoise for static file serving
- `DEBUG=False` in production

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure Stripe live keys
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Run `python manage.py collectstatic`
- [ ] Configure HTTPS

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📄 License

All rights reserved. This project is developed as a Final Year Project (FYP).

---

## 📞 Contact

- **Website**: [rohaannoor123.pythonanywhere.com](https://rohaannoor123.pythonanywhere.com)
- **Location**: Lahore, Pakistan

---

<p align="center">
  Made with ❤️ for Pakistan Tourism
</p>
