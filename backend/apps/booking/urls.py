from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('venues/', views.VenueView.as_view(), name='venues'),
    path('venues/<int:venue_id>/', views.VenueDetailView.as_view(), name='venue_detail'),
    path('venues/<int:venue_id>/availability/', views.venue_availability, name='venue_availability'),
    path('bookings/', views.BookingView.as_view(), name='bookings'),
    path('bookings/<int:booking_id>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('users/<str:user_id>/bookings/', views.user_bookings, name='user_bookings'),
]