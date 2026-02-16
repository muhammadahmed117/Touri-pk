from django.urls import path
from . import views
from .company_views import (
    company_portal, add_package, edit_package, delete_package,
    add_product, edit_product, delete_product,
    company_bookings, update_booking_status,
)

app_name = 'packages'

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('package/<slug:slug>/', views.package_detail, name='package_detail'),
    path('company/<slug:slug>/', views.company_detail, name='company_detail'),
    path('booking/create/<int:package_id>/', views.create_booking, name='create_booking'),
    path('booking/payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('booking/process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('booking/create-payment-intent/<int:booking_id>/', views.create_booking_payment_intent, name='create_booking_payment_intent'),
    path('booking/payment-success/<int:booking_id>/', views.booking_payment_success, name='booking_payment_success'),
    path('booking/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    
    # Package Reviews
    path('package/<slug:slug>/review/<int:booking_id>/', views.add_package_review, name='add_package_review'),
    
    # Company Portal
    path('company-portal/', company_portal, name='company_portal'),
    path('company-portal/add-package/', add_package, name='add_package'),
    path('company-portal/edit-package/<int:package_id>/', edit_package, name='edit_package'),
    path('company-portal/delete/<int:package_id>/', delete_package, name='delete_package'),
    
    # Company Products
    path('company-portal/add-product/', add_product, name='add_product'),
    path('company-portal/edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('company-portal/delete-product/<int:product_id>/', delete_product, name='delete_product'),
    
    # Company Bookings
    path('company-portal/bookings/', company_bookings, name='company_bookings'),
    path('company-portal/bookings/update-status/<int:booking_id>/', update_booking_status, name='update_booking_status'),
    
    # User bookings
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
