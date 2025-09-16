from rest_framework import serializers
from .models import Venue, Booking
from django.utils import timezone


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['venue_id', 'venue_name', 'description', 'capacity', 'base_rate_2h', 'base_rate_4h', 'base_rate_6h', 'base_rate_6h_plus']


class BookingSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'venue', 'venue_id', 'applicant_id', 'event_date', 'start_time', 'end_time', 
            'total_hours', 'status', 'event_details', 'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']
    
    def validate(self, data):
        """Validate booking data."""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("End time must be after start time")
            
            if start_time < timezone.now():
                raise serializers.ValidationError("Start time cannot be in the past")
        
        return data


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['venue_id', 'applicant_id', 'event_date', 'start_time', 'end_time', 'total_hours', 'event_details']


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'status', 'event_details']
