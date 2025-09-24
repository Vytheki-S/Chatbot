from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, date
import json
import uuid

from .models import (
    ChatSession, ChatMessage, ChatbotMessage, Applicant, Venue, VenueImage, 
    PriceTier, Booking, Feedback, BookingSlot, AdditionalService, PreArrangement,
    BookingService, NewPayment, OnlinePayment, ManualPayment, PaymentNotification,
    Refund, RefundBankDetails, PaymentAuditLog, PaymentInvoice, LegacyPayment,
    BankSlip, RefundRequest, JTCCHistory, JTCCFunder, JTCCFacility, JTCCMilestone, Contact
)
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer, ChatbotMessageSerializer,
    ApplicantSerializer, VenueSerializer, VenueImageSerializer, PriceTierSerializer,
    BookingSerializer, FeedbackSerializer, BookingSlotSerializer, AdditionalServiceSerializer,
    PreArrangementSerializer, BookingServiceSerializer, NewPaymentSerializer,
    OnlinePaymentSerializer, ManualPaymentSerializer, PaymentNotificationSerializer,
    RefundSerializer, RefundBankDetailsSerializer, PaymentAuditLogSerializer,
    PaymentInvoiceSerializer, LegacyPaymentSerializer, BankSlipSerializer,
    RefundRequestSerializer, JTCCHistorySerializer, JTCCFunderSerializer,
    JTCCFacilitySerializer, JTCCMilestoneSerializer, ContactSerializer,
    VenueDetailSerializer, BookingDetailSerializer
)
from .services import OpenRouterService

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """Get CSRF token for frontend"""
    return Response({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_sessions(request):
    """Get all chat sessions for the current user"""
    try:
        # Get user_id from query parameters
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sessions = ChatSession.objects.filter(user_id=user_id)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to retrieve sessions'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def send_message(request):
    """Send a message to the chatbot and get a response"""
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        
        if not message_content:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # For development, use first user or create one
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('testuser', 'test@example.com', 'password')
        
        # If user is not authenticated, use the test user
        if not request.user.is_authenticated:
            request.user = user
        
        # Get or create session
        session = ChatSession.objects.filter(user_id=user.username).first()
        if not session:
            session = ChatSession.objects.create(
                user_id=user.username
            )
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            sender_type='user',
            content=message_content
        )
        
        # Get response from OpenRouter
        openrouter_service = OpenRouterService()
        bot_response = openrouter_service.generate_response(message_content)
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            session=session,
            sender_type='admin',
            content=bot_response
        )
        
        # Update session
        session.save()
        
        return Response({
            'session_id': session.id,
            'message_id': bot_message.id,
            'response': bot_response
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_session(request, session_id):
    """Get a specific chat session"""
    try:
        session = get_object_or_404(ChatSession, id=session_id)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to retrieve session'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_sessions_by_user(request, user_id):
    """Get all chat sessions for a specific user"""
    try:
        sessions = ChatSession.objects.filter(user_id=user_id)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to retrieve sessions'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venues(request):
    """Get all venues"""
    from apps.booking.models import Venue
    venues = Venue.objects.all()
    venue_data = []
    for venue in venues:
        venue_data.append({
            'id': venue.id,
            'name': venue.venue_name,
            'capacity': venue.capacity,
            'status': venue.status,
            'description': venue.description
        })
    return Response(venue_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue_recommendations(request):
    """Get venue recommendations based on query parameters"""
    from apps.booking.models import Venue
    capacity = request.GET.get('capacity')
    status = request.GET.get('status', 'active')
    
    venues = Venue.objects.filter(status=status)
    if capacity:
        venues = venues.filter(capacity__gte=int(capacity))
    
    venue_data = []
    for venue in venues:
        venue_data.append({
            'id': venue.id,
            'name': venue.venue_name,
            'capacity': venue.capacity,
            'status': venue.status,
            'description': venue.description
        })
    return Response(venue_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy'})


# ==================== VENUE MANAGEMENT ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venues(request):
    """Get all venues with optional filtering"""
    try:
        status_filter = request.GET.get('status', 'active')
        capacity_min = request.GET.get('capacity_min')
        
        venues = Venue.objects.filter(status=status_filter)
        
        if capacity_min:
            venues = venues.filter(capacity__gte=int(capacity_min))
        
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue_detail(request, venue_id):
    """Get detailed venue information including images and price tiers"""
    try:
        venue = get_object_or_404(Venue, venue_id=venue_id)
        serializer = VenueDetailSerializer(venue)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue_recommendations(request):
    """Get venue recommendations based on query parameters"""
    try:
        capacity = request.GET.get('capacity')
        status_filter = request.GET.get('status', 'active')
        event_type = request.GET.get('event_type')
        
        venues = Venue.objects.filter(status=status_filter)
        
        if capacity:
            venues = venues.filter(capacity__gte=int(capacity))
        
        # Add more sophisticated filtering based on event type if needed
        if event_type:
            # This could be expanded with more complex logic
            pass
        
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue_availability(request, venue_id):
    """Check venue availability for specific dates"""
    try:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error': 'start_date and end_date are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check for existing bookings that overlap with the requested dates
        conflicting_bookings = BookingSlot.objects.filter(
            venue_id=venue_id,
            start_date__lte=end_date,
            end_date__gte=start_date,
            booking__booking_status__in=['confirmed', 'pending']
        )
        
        is_available = not conflicting_bookings.exists()
        
        return Response({
            'venue_id': venue_id,
            'start_date': start_date,
            'end_date': end_date,
            'is_available': is_available,
            'conflicting_bookings': conflicting_bookings.count()
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== APPLICANT MANAGEMENT ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_applicants(request):
    """Get all applicants"""
    try:
        applicants = Applicant.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_applicant(request):
    """Create a new applicant"""
    try:
        data = json.loads(request.body)
        serializer = ApplicantSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_applicant(request, applicant_id):
    """Get specific applicant details"""
    try:
        applicant = get_object_or_404(Applicant, applicant_id=applicant_id)
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== BOOKING MANAGEMENT ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_bookings(request):
    """Get all bookings with optional filtering"""
    try:
        status_filter = request.GET.get('status')
        applicant_id = request.GET.get('applicant_id')
        
        bookings = Booking.objects.all()
        
        if status_filter:
            bookings = bookings.filter(booking_status=status_filter)
        
        if applicant_id:
            bookings = bookings.filter(applicant_id=applicant_id)
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_booking_detail(request, booking_id):
    """Get detailed booking information"""
    try:
        booking = get_object_or_404(Booking, booking_id=booking_id)
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_booking(request):
    """Create a new booking"""
    try:
        data = json.loads(request.body)
        
        # Generate unique booking reference
        data['booking_reference'] = f"BK{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
        
        serializer = BookingSerializer(data=data)
        
        if serializer.is_valid():
            booking = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny])
@csrf_exempt
def update_booking_status(request, booking_id):
    """Update booking status"""
    try:
        booking = get_object_or_404(Booking, booking_id=booking_id)
        data = json.loads(request.body)
        
        new_status = data.get('booking_status')
        if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
            booking.booking_status = new_status
            booking.save()
            
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== PAYMENT MANAGEMENT ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_payments(request):
    """Get all payments with optional filtering"""
    try:
        status_filter = request.GET.get('status')
        booking_id = request.GET.get('booking_id')
        
        payments = NewPayment.objects.all()
        
        if status_filter:
            payments = payments.filter(status=status_filter)
        
        if booking_id:
            payments = payments.filter(booking_id=booking_id)
        
        serializer = NewPaymentSerializer(payments, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_payment(request):
    """Create a new payment"""
    try:
        data = json.loads(request.body)
        serializer = NewPaymentSerializer(data=data)
        
        if serializer.is_valid():
            payment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny])
@csrf_exempt
def update_payment_status(request, payment_id):
    """Update payment status"""
    try:
        payment = get_object_or_404(NewPayment, id=payment_id)
        data = json.loads(request.body)
        
        new_status = data.get('status')
        if new_status in ['PENDING', 'SUCCESS', 'FAILED', 'REFUNDED']:
            payment.status = new_status
            payment.save()
            
            serializer = NewPaymentSerializer(payment)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== ADDITIONAL SERVICES ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_additional_services(request):
    """Get all additional services"""
    try:
        services = AdditionalService.objects.all()
        serializer = AdditionalServiceSerializer(services, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_mandatory_services(request):
    """Get mandatory additional services"""
    try:
        services = AdditionalService.objects.filter(is_mandatory=True)
        serializer = AdditionalServiceSerializer(services, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== FEEDBACK ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_feedback(request):
    """Get all feedback"""
    try:
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_feedback(request):
    """Create new feedback"""
    try:
        data = json.loads(request.body)
        serializer = FeedbackSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== REFUND REQUEST ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_refund_requests(request):
    """Get all refund requests"""
    try:
        status_filter = request.GET.get('status')
        
        refund_requests = RefundRequest.objects.all()
        
        if status_filter:
            refund_requests = refund_requests.filter(status=status_filter)
        
        serializer = RefundRequestSerializer(refund_requests, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_refund_request(request):
    """Create new refund request"""
    try:
        data = json.loads(request.body)
        serializer = RefundRequestSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([AllowAny])
@csrf_exempt
def update_refund_request_status(request, refund_request_id):
    """Update refund request status"""
    try:
        refund_request = get_object_or_404(RefundRequest, id=refund_request_id)
        data = json.loads(request.body)
        
        new_status = data.get('status')
        if new_status in ['pending', 'approved', 'rejected', 'processed']:
            refund_request.status = new_status
            refund_request.processed_by = data.get('processed_by', '')
            refund_request.processed_at = timezone.now()
            refund_request.admin_notes = data.get('admin_notes', '')
            refund_request.save()
            
            serializer = RefundRequestSerializer(refund_request)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== JTCC INFORMATION ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_jtcc_history(request):
    """Get JTCC history information"""
    try:
        history = JTCCHistory.objects.first()
        if history:
            serializer = JTCCHistorySerializer(history)
            return Response(serializer.data)
        else:
            return Response({'error': 'No JTCC history found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_jtcc_funders(request):
    """Get JTCC funders information"""
    try:
        funders = JTCCFunder.objects.filter(is_active=True)
        serializer = JTCCFunderSerializer(funders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_jtcc_facilities(request):
    """Get JTCC facilities information"""
    try:
        facilities = JTCCFacility.objects.filter(is_available=True)
        serializer = JTCCFacilitySerializer(facilities, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_jtcc_milestones(request):
    """Get JTCC milestones information"""
    try:
        milestones = JTCCMilestone.objects.all()
        serializer = JTCCMilestoneSerializer(milestones, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_jtcc_comprehensive_info(request):
    """Get comprehensive JTCC information"""
    try:
        history = JTCCHistory.objects.first()
        funders = JTCCFunder.objects.filter(is_active=True)
        facilities = JTCCFacility.objects.filter(is_available=True)
        milestones = JTCCMilestone.objects.all()[:5]  # Get latest 5 milestones
        
        return Response({
            'history': JTCCHistorySerializer(history).data if history else None,
            'funders': JTCCFunderSerializer(funders, many=True).data,
            'facilities': JTCCFacilitySerializer(facilities, many=True).data,
            'recent_milestones': JTCCMilestoneSerializer(milestones, many=True).data
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== CONTACT ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_contacts(request):
    """Get contact information"""
    try:
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_contact(request):
    """Create new contact information"""
    try:
        data = json.loads(request.body)
        serializer = ContactSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== ANALYTICS AND DASHBOARD ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_booking_analytics(request):
    """Get booking analytics for dashboard"""
    try:
        total_bookings = Booking.objects.count()
        confirmed_bookings = Booking.objects.filter(booking_status='confirmed').count()
        pending_bookings = Booking.objects.filter(booking_status='pending').count()
        cancelled_bookings = Booking.objects.filter(booking_status='cancelled').count()
        
        total_revenue = Booking.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        bookings_by_status = Booking.objects.values('booking_status').annotate(
            count=Count('booking_id')
        )
        
        return Response({
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'pending_bookings': pending_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_revenue': float(total_revenue),
            'bookings_by_status': list(bookings_by_status)
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue_analytics(request):
    """Get venue analytics"""
    try:
        total_venues = Venue.objects.count()
        active_venues = Venue.objects.filter(status='active').count()
        
        venue_usage = BookingSlot.objects.values('venue__venue_name').annotate(
            booking_count=Count('booking_id')
        ).order_by('-booking_count')
        
        return Response({
            'total_venues': total_venues,
            'active_venues': active_venues,
            'venue_usage': list(venue_usage)
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== SEARCH ENDPOINTS ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def search_bookings(request):
    """Search bookings by various criteria"""
    try:
        query = request.GET.get('q', '')
        booking_reference = request.GET.get('booking_reference')
        applicant_name = request.GET.get('applicant_name')
        
        bookings = Booking.objects.all()
        
        if query:
            bookings = bookings.filter(
                Q(booking_reference__icontains=query) |
                Q(applicant__applicant_name__icontains=query) |
                Q(event_details__icontains=query)
            )
        
        if booking_reference:
            bookings = bookings.filter(booking_reference__icontains=booking_reference)
        
        if applicant_name:
            bookings = bookings.filter(applicant__applicant_name__icontains=applicant_name)
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_venues(request):
    """Search venues by various criteria"""
    try:
        query = request.GET.get('q', '')
        capacity_min = request.GET.get('capacity_min')
        capacity_max = request.GET.get('capacity_max')
        
        venues = Venue.objects.filter(status='active')
        
        if query:
            venues = venues.filter(
                Q(venue_name__icontains=query) |
                Q(description__icontains=query)
            )
        
        if capacity_min:
            venues = venues.filter(capacity__gte=int(capacity_min))
        
        if capacity_max:
            venues = venues.filter(capacity__lte=int(capacity_max))
        
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([AllowAny])
def test_endpoint(request):
    """Simple test endpoint"""
    return Response({'status': 'success', 'message': 'Server is working!'})
