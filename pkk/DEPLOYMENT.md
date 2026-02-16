# Deployment Checklist for TouriPK

## Pre-Deployment Steps

### 1. Environment Configuration
- [ ] Copy `.env.example` to `.env` on production server
- [ ] Update `SECRET_KEY` with a new secure key
- [ ] Set `DEBUG=False` for production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up database credentials (if using PostgreSQL/MySQL)

### 2. Database Setup
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Load initial data if needed

### 3. Static Files
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Configure web server (Nginx/Apache) to serve static files
- [ ] Configure media files serving

### 4. Security Settings
- [ ] Ensure `DEBUG=False`
- [ ] Configure HTTPS/SSL
- [ ] Set secure cookie settings
- [ ] Configure CSRF trusted origins
- [ ] Set up proper file permissions

### 5. Chatbot Configuration (Optional)
- [ ] Add DeepSeek API key in `chatbot/config.py`
- [ ] Test chatbot functionality

### 6. Email Configuration (Optional)
- [ ] Configure email backend for notifications
- [ ] Set up SMTP settings

### 7. Company Setup
- [ ] Ensure company logos are uploaded in `media/Logos/`
- [ ] Verify active companies are correct
- [ ] Check company approval status

### 8. Testing
- [ ] Test user registration and login
- [ ] Test product purchase flow
- [ ] Test package booking
- [ ] Test custom calculator
- [ ] Test weather feature
- [ ] Test chatbot
- [ ] Test company portal
- [ ] Check all static assets load correctly
- [ ] Test on different browsers
- [ ] Test responsive design on mobile

### 9. Performance
- [ ] Enable caching if needed
- [ ] Optimize database queries
- [ ] Compress static files
- [ ] Set up CDN for static/media files (optional)

### 10. Backup
- [ ] Set up database backups
- [ ] Set up media files backup
- [ ] Document backup recovery process

## Production Server Setup

### Web Server (Nginx example)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/touripk/static_root/;
    }

    location /media/ {
        alias /path/to/touripk/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Application Server (Gunicorn)
```bash
pip install gunicorn
gunicorn touripk.wsgi:application --bind 127.0.0.1:8000
```

## Post-Deployment

- [ ] Monitor error logs
- [ ] Check application performance
- [ ] Verify all features working
- [ ] Set up monitoring (optional)
- [ ] Configure backup automation

## Important Notes

1. **Never commit `.env` file** - Contains sensitive information
2. **Keep `db.sqlite3` secure** - Contains all application data
3. **Media files** - Ensure proper permissions and backups
4. **Secret Key** - Generate new one for production
5. **Debug Mode** - Always `False` in production

## Support

For issues or questions, contact the development team.
