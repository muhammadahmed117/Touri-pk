from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    # Customer URLs
    path('create/', views.create_ticket, name='create_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<str:ticket_id>/escalate/', views.escalate_ticket, name='escalate_ticket'),

    # Company URLs
    path('company-tickets/', views.company_tickets, name='company_tickets'),

    # Shared (company/admin)
    path('ticket/<str:ticket_id>/resolve/', views.resolve_ticket, name='resolve_ticket'),

    # Admin URLs
    path('admin-tickets/', views.admin_tickets, name='admin_tickets'),
]
