# OAuth Social Authentication Setup Guide

## Overview
Your website now supports social login with Google and Facebook! Users can sign in/register using their existing Google or Facebook accounts.

## What's Been Completed ✅

1. **Package Installation**: `django-allauth` installed
2. **Settings Configuration**: OAuth providers configured in `settings.py`
3. **URL Routing**: Social auth URLs added to `urls.py`
4. **Templates Updated**: Login and Register pages now have "Continue with Google" and "Continue with Facebook" buttons
5. **Database Migrations**: All necessary tables created

## Next Steps: Getting OAuth Credentials

### Step 1: Google OAuth Setup

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project** (or select existing)
   - Click "Select a project" → "New Project"
   - Name: "TouriPK Website" (or your choice)
   - Click "Create"

3. **Enable Google+ API**
   - In the Dashboard, click "Enable APIs and Services"
   - Search for "Google+ API"
   - Click "Enable"

4. **Create OAuth Credentials**
   - Go to "Credentials" in left sidebar
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - User Type: External
     - App name: TouriPK
     - User support email: your email
     - Authorized domains: yourdomain.com (leave empty for localhost)
   - Application type: "Web application"
   - Name: "TouriPK OAuth"
   - Authorized JavaScript origins:
     - `http://localhost:8000`
     - `http://127.0.0.1:8000`
     - Add your production domain when ready
   - Authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/`
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
     - Add your production domain when ready
   - Click "Create"

5. **Copy Your Credentials**
   - You'll see "Client ID" and "Client Secret"
   - **SAVE THESE SECURELY!**

### Step 2: Facebook OAuth Setup

1. **Go to Facebook Developers**
   - Visit: https://developers.facebook.com/

2. **Create an App**
   - Click "My Apps" → "Create App"
   - Use case: "Other"
   - App type: "Consumer"
   - App name: "TouriPK"
   - Contact email: your email
   - Click "Create App"

3. **Add Facebook Login**
   - In your app dashboard, find "Facebook Login"
   - Click "Set Up"
   - Choose "Web" platform
   - Site URL: `http://localhost:8000` (for testing)

4. **Configure OAuth Redirect URIs**
   - Go to Facebook Login → Settings
   - Valid OAuth Redirect URIs:
     - `http://localhost:8000/accounts/facebook/login/callback/`
     - `http://127.0.0.1:8000/accounts/facebook/login/callback/`
     - Add your production domain when ready
   - Save Changes

5. **Get App Credentials**
   - Go to Settings → Basic
   - Copy "App ID" and "App Secret"
   - **SAVE THESE SECURELY!**

### Step 3: Configure Environment Variables

1. **Create/Update `.env` file** in your project root (`d:\website\pkk\`):

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Facebook OAuth
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here
```

2. **Replace the placeholder values** with your actual credentials from Steps 1 and 2

### Step 4: Configure Social Applications in Django Admin

1. **Create a Superuser** (if you haven't already):
```bash
python manage.py createsuperuser
```

2. **Login to Django Admin**:
   - Visit: http://localhost:8000/admin/
   - Login with your superuser credentials

3. **Add Google Social Application**:
   - Go to "Sites" → Click on "example.com" → Change domain to "localhost:8000"
   - Go to "Social applications" → "Add social application"
   - Provider: Google
   - Name: Google OAuth
   - Client ID: (paste your Google Client ID)
   - Secret Key: (paste your Google Client Secret)
   - Sites: Select "localhost:8000" and move it to "Chosen sites"
   - Save

4. **Add Facebook Social Application**:
   - Go to "Social applications" → "Add social application"
   - Provider: Facebook
   - Name: Facebook OAuth
   - Client ID: (paste your Facebook App ID)
   - Secret Key: (paste your Facebook App Secret)
   - Key: (leave empty)
   - Sites: Select "localhost:8000" and move it to "Chosen sites"
   - Save

### Step 5: Test Your OAuth Setup

1. **Restart your Django server**:
```bash
python manage.py runserver
```

2. **Test Google Login**:
   - Go to http://localhost:8000/users/login/
   - Click "Continue with Google"
   - You should be redirected to Google login
   - After authentication, you'll be redirected back to your site

3. **Test Facebook Login**:
   - Go to http://localhost:8000/users/login/
   - Click "Continue with Facebook"
   - You should be redirected to Facebook login
   - After authentication, you'll be redirected back to your site

## Troubleshooting

### "redirect_uri_mismatch" Error
- Check that your redirect URIs in Google/Facebook match exactly
- Make sure you're using the correct domain (localhost:8000 or 127.0.0.1:8000)

### "Invalid Client ID" Error
- Verify your credentials in `.env` file
- Check that you've configured the Social Applications in Django admin
- Make sure SITE_ID=1 in settings.py matches your site

### OAuth Buttons Not Working
- Ensure django-allauth is installed: `pip install django-allauth`
- Check that migrations are applied: `python manage.py migrate`
- Verify allauth URLs are included in `urls.py`

### Settings Deprecation Warnings
These are informational warnings from newer allauth versions. Your setup will still work, but you can update settings later if needed.

## Production Deployment

When deploying to production:

1. **Update OAuth Redirect URIs** in Google and Facebook dashboards:
   - Add your production domain: `https://yourdomain.com/accounts/google/login/callback/`
   - Add your production domain: `https://yourdomain.com/accounts/facebook/login/callback/`

2. **Update Site in Django Admin**:
   - Change domain from "localhost:8000" to your actual domain

3. **Use HTTPS**:
   - Both Google and Facebook require HTTPS in production
   - Set up SSL certificate for your domain

4. **Secure Your Secrets**:
   - Never commit `.env` file to version control
   - Use environment variables or secure secret management
   - Add `.env` to `.gitignore`

## Security Notes

- **Never share your Client Secrets or App Secrets publicly**
- Keep your `.env` file secure and out of version control
- Use different credentials for development and production
- Regularly rotate your OAuth credentials
- Enable 2FA on your Google and Facebook developer accounts

## Additional Resources

- [django-allauth Documentation](https://docs.allauth.org/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login)

## Need Help?

If you encounter issues:
1. Check the Django logs for error messages
2. Verify all credentials are correct
3. Ensure redirect URIs match exactly
4. Test with incognito/private browsing mode
5. Check the browser console for JavaScript errors

---

**Status**: OAuth setup is complete! Just add your credentials and configure the social applications in Django admin to start using social login.
