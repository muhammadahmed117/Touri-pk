from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('send/', views.send_message, name='send_message'),
    path('history/<int:session_id>/', views.get_chat_history, name='chat_history'),
]