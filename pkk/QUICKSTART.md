# TouriPK - Quick Start Guide

## What's Included

This is a complete Django tourism platform with:

✅ User authentication system
✅ Destinations catalog
✅ Tour packages marketplace
✅ Products shop with shopping cart
✅ Custom package cost calculator
✅ Weather information
✅ AI travel chatbot
✅ Company registration portal
✅ Admin dashboard

## Installation (5 Minutes)

1. **Install Python 3.12+** (if not installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env`
   - No changes needed for local testing

4. **Setup database:**
   ```bash
   python manage.py migrate
   ```

5. **Create admin account:**
   ```bash
   python manage.py createsuperuser
   ```
   Enter username, email, and password when prompted.

6. **Start server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the site:**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Default Setup

The application includes:
- 2 verified tour companies (Northway Tourism, Smile Miles Tour)
- 4 products with images
- Sample destinations
- Fully functional shopping cart
- Custom package calculator for 3 destinations

## Admin Features

Login to `/admin/` to:
- Manage destinations and products
- Approve company registrations
- View and manage orders
- Configure site settings

## User Features

Users can:
- Browse destinations and packages
- Shop products with cart and checkout
- Calculate custom package costs
- Check destination weather
- Chat with AI travel assistant
- Register as tour operator

## Configuration (Optional)

### AI Chatbot
Edit `chatbot/config.py` and add your DeepSeek API key from https://platform.deepseek.com/

### Database
For production, update `.env` with PostgreSQL/MySQL credentials

### Email
Configure email backend in settings for notifications

## Deployment

See `DEPLOYMENT.md` for complete production deployment guide.

## Support

- Check `README.md` for detailed documentation
- Review `DEPLOYMENT.md` for deployment steps
- All code is well-commented for easy understanding

## Important Files

- `.env` - Environment configuration (do not commit to git)
- `db.sqlite3` - Database file (backup regularly)
- `media/` - Uploaded files (backup regularly)
- `requirements.txt` - Python dependencies

## Next Steps

1. Login to admin panel
2. Explore the features
3. Customize content as needed
4. Add more destinations/products
5. Configure for production deployment

Enjoy your TouriPK platform! 🎉
