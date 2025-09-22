from django.urls import path
from . import views

urlpatterns = [
    # Chat endpoints
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('chat/', views.send_message, name='send_message'),
    path('send-message/', views.send_message, name='send_message_alt'),
    path('users/<str:user_id>/sessions/', views.get_sessions_by_user, name='get_chat_sessions'),
    path('sessions/delete/<int:session_id>/', views.get_session, name='delete_chat_session'),
    
    # Venue Management endpoints
    path('venues/', views.get_venues, name='get_venues'),
    path('venues/<int:venue_id>/', views.get_venue_detail, name='get_venue_detail'),
    path('venues/recommendations/', views.get_venue_recommendations, name='get_venue_recommendations'),
    path('venues/<int:venue_id>/availability/', views.get_venue_availability, name='get_venue_availability'),
    path('venues/search/', views.search_venues, name='search_venues'),
    
    # Applicant Management endpoints
    path('applicants/', views.get_applicants, name='get_applicants'),
    path('applicants/create/', views.create_applicant, name='create_applicant'),
    path('applicants/<int:applicant_id>/', views.get_applicant, name='get_applicant'),
    
    # Booking Management endpoints
    path('bookings/', views.get_bookings, name='get_bookings'),
    path('bookings/<int:booking_id>/', views.get_booking_detail, name='get_booking_detail'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/status/', views.update_booking_status, name='update_booking_status'),
    path('bookings/search/', views.search_bookings, name='search_bookings'),
    
    # Payment Management endpoints
    path('payments/', views.get_payments, name='get_payments'),
    path('payments/create/', views.create_payment, name='create_payment'),
    path('payments/<int:payment_id>/status/', views.update_payment_status, name='update_payment_status'),
    
    # Additional Services endpoints
    path('services/', views.get_additional_services, name='get_additional_services'),
    path('services/mandatory/', views.get_mandatory_services, name='get_mandatory_services'),
    
    # Feedback endpoints
    path('feedback/', views.get_feedback, name='get_feedback'),
    path('feedback/create/', views.create_feedback, name='create_feedback'),
    
    # Refund Request endpoints
    path('refund-requests/', views.get_refund_requests, name='get_refund_requests'),
    path('refund-requests/create/', views.create_refund_request, name='create_refund_request'),
    path('refund-requests/<int:refund_request_id>/status/', views.update_refund_request_status, name='update_refund_request_status'),
    
    # JTCC Information endpoints
    path('jtcc/history/', views.get_jtcc_history, name='get_jtcc_history'),
    path('jtcc/funders/', views.get_jtcc_funders, name='get_jtcc_funders'),
    path('jtcc/facilities/', views.get_jtcc_facilities, name='get_jtcc_facilities'),
    path('jtcc/milestones/', views.get_jtcc_milestones, name='get_jtcc_milestones'),
    path('jtcc/info/', views.get_jtcc_comprehensive_info, name='get_jtcc_comprehensive_info'),
    
    # Contact endpoints
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('contacts/create/', views.create_contact, name='create_contact'),
    
    # Analytics and Dashboard endpoints
    path('analytics/bookings/', views.get_booking_analytics, name='get_booking_analytics'),
    path('analytics/venues/', views.get_venue_analytics, name='get_venue_analytics'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
]