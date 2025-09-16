from django.urls import path
from . import views

urlpatterns = [
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('chat/', views.send_message, name='send_message'),
    path('send-message/', views.send_message, name='send_message_alt'),
    path('users/<str:user_id>/sessions/', views.get_chat_sessions, name='get_chat_sessions'),
    path('sessions/delete/<int:session_id>/', views.delete_chat_session, name='delete_chat_session'),
    path('venues/', views.get_venues, name='get_venues'),
    path('venues/recommendations/', views.get_venue_recommendations, name='get_venue_recommendations'),
    path('health/', views.health_check, name='health_check'),
]