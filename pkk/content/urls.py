from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('packages/', views.tour_packages, name='tour_packages'),
    path('products/', views.product_list, name='product_list'),
    path('calculator/', views.custom_package, name='cost_calculator'),
    path('custom-package/', views.custom_package, name='custom_package'),
    path('custom-package/payment/<int:order_id>/', views.custom_package_payment, name='custom_package_payment'),
    path('custom-package/create-payment-intent/<int:order_id>/', views.create_payment_intent, name='create_payment_intent'),
    path('custom-package/payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('custom-package/confirmation/<int:order_id>/', views.custom_package_confirmation, name='custom_package_confirmation'),
    path('my-custom-packages/', views.my_custom_packages, name='my_custom_packages'),
    path('api/destination-costs/', views.get_destination_costs, name='get_destination_costs'),
    path('api/admin-notifications/', views.admin_notifications_api, name='admin_notifications_api'),
    path('api/mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('check-weather/', views.check_weather, name='check_weather'),
    
    # Cart and Order URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Product Reviews
    path('product/<int:product_id>/review/<int:order_id>/', views.add_product_review, name='add_product_review'),
]