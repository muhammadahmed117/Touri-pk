from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django_ratelimit.decorators import ratelimit
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm, CompanyUserRegistrationForm
from content.models import Destination, Product
from packages.models import Company, Booking
import logging

logger = logging.getLogger(__name__)


class UserRegisterView(CreateView):
    """Secure user registration with proper validation"""
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(ratelimit(key='ip', rate='15/h', method='POST', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Save user with hashed password and log the registration"""
        try:
            user = form.save(commit=False)
            user.email = user.email.lower()  # Normalize email
            # Username is now provided by the user in the form
            # Set full_name from username
            user.full_name = user.username
            user.user_type = 'user'  # Explicitly set as regular user
            user.save()
            
            logger.info(f"New user registered: {user.username} ({user.email})")
            
            messages.success(
                self.request,
                'Registration successful! Your account has been created. Please login to continue.'
            )
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            messages.error(self.request, 'Registration failed. Please try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submission"""
        logger.warning(f"Invalid registration attempt: {form.errors}")
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Your Account'
        return context


class CompanyRegisterView(CreateView):
    """Registration view for company/tour operator accounts"""
    model = CustomUser
    form_class = CompanyUserRegistrationForm
    template_name = 'users/company_register.html'
    success_url = reverse_lazy('login')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(ratelimit(key='ip', rate='10/h', method='POST', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """Include request.FILES for image uploads"""
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

    def form_valid(self, form):
        """Create user account AND company object together"""
        try:
            # Save user with company type
            user = form.save(commit=False)
            user.email = form.cleaned_data['company_email'].lower()
            user.full_name = form.cleaned_data['company_name']
            user.user_type = 'company'
            user.save()

            # Create the Company object
            company_name = form.cleaned_data['company_name']
            base_slug = slugify(company_name)

            # Handle slug collision
            slug = base_slug
            counter = 1
            while Company.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            Company.objects.create(
                owner=user,
                name=company_name,
                slug=slug,
                description=form.cleaned_data['company_description'],
                email=form.cleaned_data['company_email'],
                phone=form.cleaned_data['company_phone'],
                cnic_front=form.cleaned_data.get('cnic_front'),
                cnic_back=form.cleaned_data.get('cnic_back'),
                approval_status='pending',
            )

            logger.info(f"New company registered: {company_name} by {user.username}")

            messages.success(
                self.request,
                'Registration successful! Your approval request has been sent to admin. '
                'You will receive a notification once your company is approved. Please login to continue.'
            )
            return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Company registration error: {str(e)}")
            messages.error(self.request, 'Registration failed. Please try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submission"""
        logger.warning(f"Invalid company registration attempt: {form.errors}")
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register Your Company'
        return context


class UserLoginView(FormView):
    """Secure login view with rate limiting and session management"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('dashboard')

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(ratelimit(key='ip', rate='10/5m', method='POST', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        """Authenticate and login user with session management"""
        try:
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Authenticate user
            user = authenticate(self.request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    
                    # Set session expiry based on remember_me
                    if remember_me:
                        self.request.session.set_expiry(2592000)  # 30 days
                    else:
                        self.request.session.set_expiry(0)  # Browser close
                    
                    logger.info(f"User logged in: {user.email}")
                    
                    # Check if company user and approval status
                    if user.user_type == 'company':
                        try:
                            from packages.models import Company
                            company = Company.objects.filter(owner=user).first()
                            if company and company.approval_status == 'pending':
                                messages.warning(
                                    self.request, 
                                    'Your company registration is pending admin approval. '
                                    'You will be able to access the company portal once your company is approved.'
                                )
                                # Logout the user since they can't access company features yet
                                from django.contrib.auth import logout
                                logout(self.request)
                                return self.form_invalid(form)
                            elif company and company.approval_status == 'rejected':
                                messages.error(
                                    self.request,
                                    f'Your company registration was rejected. Reason: {company.rejection_reason or "Please contact admin for details."}'
                                )
                                from django.contrib.auth import logout
                                logout(self.request)
                                return self.form_invalid(form)
                        except Exception as e:
                            logger.error(f"Company status check error: {str(e)}")
                    
                    messages.success(self.request, f'Welcome, {user.full_name}!')
                    
                    # Redirect based on user type
                    next_url = self.request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    elif user.user_type == 'company':
                        return redirect('packages:company_portal')
                    else:
                        return redirect(self.success_url)
                else:
                    messages.error(self.request, 'Your account has been disabled.')
                    logger.warning(f"Disabled account login attempt: {username}")
            else:
                messages.error(self.request, 'Invalid email or password.')
                logger.warning(f"Failed login attempt for: {username}")
            
            return self.form_invalid(form)
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            messages.error(self.request, 'Login failed. Please try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid login"""
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login to Your Account'
        return context


@login_required
def dashboard(request):
    """User dashboard — redirects company users to company portal"""
    # Redirect company users to their portal
    if request.user.user_type == 'company':
        return redirect('packages:company_portal')

    try:
        destinations = Destination.objects.all()
        products = Product.objects.all()
        
        # Get user's recent bookings with related data
        recent_bookings = Booking.objects.filter(
            user=request.user
        ).select_related(
            'package', 'package__company'
        ).order_by('-created_at')[:5]
        
        # Get booking statistics
        total_bookings = Booking.objects.filter(user=request.user).count()
        confirmed_bookings = Booking.objects.filter(
            user=request.user, status='confirmed'
        ).count()
        pending_bookings = Booking.objects.filter(
            user=request.user, status='pending'
        ).count()
        
        return render(request, 'users/dashboard.html', {
            'destinations': destinations,
            'products': products,
            'recent_bookings': recent_bookings,
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'pending_bookings': pending_bookings,
        })
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        messages.error(request, 'Error loading dashboard data.')
        return render(request, 'users/dashboard.html', {})

