from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class Applicant(models.Model):
    """Applicant information for bookings"""
    ORGANIZATION_TYPE_CHOICES = [
        ('corporate_business', 'Corporate / Business'),
        ('educational_institution', 'Educational Institution'),
        ('non_profit_ngo', 'Non-Profit / NGO'),
        ('government_public_sector', 'Government / Public Sector'),
        ('private_individual', 'Private Individual'),
        ('religious_organization', 'Religious Organization'),
        ('entertainment_event_management', 'Entertainment / Event Management'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applicants')
    applicant_name = models.CharField(max_length=200, help_text="Name from booking form")
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPE_CHOICES, default='other', help_text="Type of organization")
    organization = models.CharField(max_length=200, help_text="Organization/Institute name")
    contact_no = models.CharField(max_length=20, help_text="Contact number")
    email = models.EmailField(max_length=100, help_text="Email address")
    
    class Meta:
        db_table = 'booking_applicant'
    
    def __str__(self):
        return f"{self.applicant_name} - {self.organization}"


class Venue(models.Model):
    """Venue information"""
    VENUE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    venue_name = models.CharField(max_length=100, help_text="Name of venue")
    capacity = models.IntegerField(help_text="Maximum capacity")
    status = models.CharField(max_length=20, choices=VENUE_STATUS_CHOICES, default='active', help_text="Venue availability status")
    image = models.CharField(max_length=255, blank=True, null=True, help_text="Image file path/URL")
    description = models.TextField(blank=True, null=True, help_text="Venue description")
    
    class Meta:
        db_table = 'venues'
    
    def __str__(self):
        return self.venue_name


class VenueImage(models.Model):
    """Venue image gallery"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='venue_images')
    image_url = models.CharField(max_length=500, help_text="Image file path/URL")
    display_order = models.IntegerField(default=0, help_text="Order for displaying images")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="When image was uploaded")
    
    class Meta:
        db_table = 'booking_venueimage'
        ordering = ['display_order', 'uploaded_at']
    
    def __str__(self):
        return f"{self.venue.venue_name} - Image {self.id}"


class PriceTier(models.Model):
    """Price tiers for different durations"""
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='price_tiers')
    duration = models.IntegerField(help_text="Duration in hours (2, 4, 6, 12)")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Rate for this duration")
    
    class Meta:
        db_table = 'booking_pricetier'
    
    def __str__(self):
        return f"{self.venue.venue_name} - {self.duration}h - ${self.price}"


class Booking(models.Model):
    """Main booking model without approval_status"""
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    
    EVENT_TYPE_CHOICES = [
        ('government', 'Government Events'),
        ('corporate', 'Corporate Events'),
        ('educational', 'Educational Events'),
        ('cultural', 'Cultural Programs'),
        ('exhibitions', 'Exhibitions & Fairs'),
        ('community', 'Community Gatherings'),
        ('competitions', 'Competitions & Award Ceremonies'),
        ('workshops', 'Workshops & Training'),
        ('lectures', 'Public Lectures & Keynote Talks'),
        ('music', 'Music Concert'),
        ('other', 'Other'),
    ]
    
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    booking_reference = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text="Human-readable reference")
    event_types = models.JSONField(default=list, help_text="List of selected event types")
    custom_event_type = models.CharField(max_length=200, blank=True, null=True, help_text="Custom event type if 'other' is selected")
    event_details = models.TextField(blank=True, null=True, help_text="Details of event")
    additional_notes = models.TextField(blank=True, null=True, help_text="Additional notes or special requests")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Total booking cost")
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending', help_text="Booking status")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', help_text="Payment status")
    is_public = models.BooleanField(default=False, help_text="Whether event is public")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When booking was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update time")
    
    class Meta:
        db_table = 'booking_booking'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking_reference} - {self.applicant.applicant_name}"


class BookingSlot(models.Model):
    """Time slots for bookings"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='slots')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='booking_slots')
    tier = models.ForeignKey(PriceTier, on_delete=models.CASCADE, related_name='booking_slots')
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(help_text="End date")
    start_time = models.TimeField(help_text="Start time")
    end_time = models.TimeField(help_text="End time")
    venue_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost for this venue slot")
    isfullday = models.BooleanField(default=False, help_text="Whether this is a full day booking")
    
    class Meta:
        db_table = 'booking_bookingslot'
    
    def __str__(self):
        return f"{self.booking.booking_reference} - {self.venue.venue_name} - {self.start_date}"


class AdditionalService(models.Model):
    """Additional services available"""
    service_name = models.CharField(max_length=100, help_text="Service name")
    basic_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base rate for service")
    extra_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Additional rate per extra hour")
    is_mandatory = models.BooleanField(default=False, help_text="Whether service is required")
    
    class Meta:
        db_table = 'booking_additionalservice'
    
    def __str__(self):
        return self.service_name


class PreArrangement(models.Model):
    """Pre-arrangement scheduling"""
    ARRANGEMENT_TYPE_CHOICES = [
        ('setup', 'Setup'),
        ('rehearsal', 'Rehearsal'),
        ('breakdown', 'Breakdown'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='pre_arrangements')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='pre_arrangements')
    arrangement_type = models.CharField(max_length=20, choices=ARRANGEMENT_TYPE_CHOICES, help_text="Type of arrangement")
    date = models.DateField(help_text="Arrangement date")
    start_time = models.TimeField(help_text="Start time")
    end_time = models.TimeField(help_text="End time")
    notes = models.TextField(blank=True, null=True, help_text="Special instructions")
    
    class Meta:
        db_table = 'booking_prearrangement'
    
    def __str__(self):
        return f"{self.booking.booking_reference} - {self.arrangement_type} - {self.date}"


class BookingService(models.Model):
    """Services selected for a booking"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_services')
    slot = models.ForeignKey(BookingSlot, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE, related_name='booking_services')
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, help_text="Hours service is needed")
    service_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost for this service")
    
    class Meta:
        db_table = 'booking_bookingservice'
    
    def __str__(self):
        return f"{self.booking.booking_reference} - {self.service.service_name}"