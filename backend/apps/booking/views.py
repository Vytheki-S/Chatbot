from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializers import (
    VenueSerializer, 
    BookingSerializer, 
    BookingCreateSerializer,
    BookingUpdateSerializer
)
from .models import Venue, Booking


class VenueView(APIView):
    """API view for venue operations."""
    
    def get(self, request):
        """Get all available venues with optional filtering."""
        venues = Venue.objects.all()  # All venues are available in our system
        
        # Filter by capacity
        min_capacity = request.query_params.get('min_capacity')
        if min_capacity:
            try:
                venues = venues.filter(capacity__gte=int(min_capacity))
            except ValueError:
                pass
        
        # Filter by max rate (using 2h rate as reference)
        max_rate = request.query_params.get('max_rate')
        if max_rate:
            try:
                venues = venues.filter(base_rate_2h__lte=float(max_rate))
            except ValueError:
                pass
        
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new venue."""
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VenueDetailView(APIView):
    """API view for individual venue operations."""
    
    def get(self, request, venue_id):
        """Get a specific venue."""
        venue = get_object_or_404(Venue, venue_id=venue_id)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)
    
    def put(self, request, venue_id):
        """Update a venue."""
        venue = get_object_or_404(Venue, venue_id=venue_id)
        serializer = VenueSerializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, venue_id):
        """Delete a venue."""
        venue = get_object_or_404(Venue, venue_id=venue_id)
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingView(APIView):
    """API view for booking operations."""
    
    def get(self, request):
        """Get bookings with optional filtering."""
        user_id = request.query_params.get('user_id')
        status_filter = request.query_params.get('status')
        
        bookings = Booking.objects.all()
        
        if user_id:
            bookings = bookings.filter(applicant_id=user_id)
        
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new booking."""
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if venue is available
            venue_id = serializer.validated_data['venue_id']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            
            # Check for conflicts
            conflicts = Booking.objects.filter(
                venue_id=venue_id,
                status__in=['pending', 'approved'],
                event_date=serializer.validated_data['event_date'],
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if conflicts.exists():
                return Response(
                    {'error': 'Venue is not available for the selected time slot'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create booking
            booking_data = serializer.validated_data.copy()
            booking = Booking.objects.create(**booking_data)
            
            response_serializer = BookingSerializer(booking)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailView(APIView):
    """API view for individual booking operations."""
    
    def get(self, request, booking_id):
        """Get a specific booking."""
        booking = get_object_or_404(Booking, booking_id=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
    def put(self, request, booking_id):
        """Update a booking."""
        booking = get_object_or_404(Booking, booking_id=booking_id)
        serializer = BookingUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = BookingSerializer(booking)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, booking_id):
        """Cancel a booking."""
        booking = get_object_or_404(Booking, booking_id=booking_id)
        if booking.status == 'approved':
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Booking cancelled successfully'})
        elif booking.status == 'cancelled':
            return Response({'error': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Cannot cancel this booking'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def venue_availability(request, venue_id):
    """Check venue availability for a specific time slot."""
    start_time = request.query_params.get('start_time')
    end_time = request.query_params.get('end_time')
    
    if not start_time or not end_time:
        return Response(
            {'error': 'start_time and end_time are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        start_time = timezone.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_time = timezone.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    except ValueError:
        return Response(
            {'error': 'Invalid datetime format. Use ISO format.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    venue = get_object_or_404(Venue, venue_id=venue_id)
    
    # Check for conflicts
    conflicts = Booking.objects.filter(
        venue_id=venue_id,
        status__in=['pending', 'approved'],
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    
    is_available = not conflicts.exists()
    
    return Response({
        'venue_id': venue_id,
        'venue_name': venue.venue_name,
        'start_time': start_time,
        'end_time': end_time,
        'is_available': is_available,
        'conflicts': conflicts.count() if not is_available else 0
    })


@api_view(['GET'])
def user_bookings(request, user_id):
    """Get all bookings for a specific user."""
    bookings = Booking.objects.filter(applicant_id=user_id).order_by('-created_at')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)