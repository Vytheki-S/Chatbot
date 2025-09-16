from django.db import models
from django.utils import timezone
from decimal import Decimal


class Venue(models.Model):
    """Venue model matching existing venues table."""
    venue_id = models.AutoField(primary_key=True, db_column='venue_id')
    venue_name = models.CharField(max_length=100, db_column='venue_name')
    capacity = models.IntegerField(db_column='capacity')
    base_rate_2h = models.DecimalField(max_digits=10, decimal_places=2, db_column='base_rate_2h')
    base_rate_4h = models.DecimalField(max_digits=10, decimal_places=2, db_column='base_rate_4h')
    base_rate_6h = models.DecimalField(max_digits=10, decimal_places=2, db_column='base_rate_6h')
    base_rate_6h_plus = models.DecimalField(max_digits=10, decimal_places=2, db_column='base_rate_6h_plus')
    description = models.TextField(db_column='description')
    
    class Meta:
        db_table = 'venues'
        ordering = ['venue_name']
    
    def __str__(self):
        return self.venue_name
    
    @property
    def name(self):
        """Alias for venue_name for backward compatibility"""
        return self.venue_name
    
    @property
    def hourly_rate(self):
        """Calculate average hourly rate for backward compatibility"""
        return (self.base_rate_2h + self.base_rate_4h + self.base_rate_6h + self.base_rate_6h_plus) / 4
    
    @property
    def is_available(self):
        """Always return True for now - can be enhanced later"""
        return True


class Booking(models.Model):
    """Booking model matching existing bookings table."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_id = models.AutoField(primary_key=True, db_column='booking_id')
    applicant_id = models.IntegerField(db_column='applicant_id')
    org_id = models.IntegerField(db_column='org_id')
    event_type_id = models.IntegerField(db_column='event_type_id')
    venue_id = models.IntegerField(db_column='venue_id')
    event_date = models.DateField(db_column='event_date')
    start_time = models.TimeField(db_column='start_time')
    end_time = models.TimeField(db_column='end_time')
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, db_column='total_hours')
    event_details = models.TextField(db_column='event_details')
    invitation_path = models.CharField(max_length=255, db_column='invitation_path', blank=True)
    pre_arrangement_date = models.DateField(db_column='pre_arrangement_date', null=True, blank=True)
    pre_arrangement_start = models.TimeField(db_column='pre_arrangement_start', null=True, blank=True)
    pre_arrangement_end = models.TimeField(db_column='pre_arrangement_end', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_column='status')
    permission_granted = models.BooleanField(default=False, db_column='permission_granted')
    granted_by = models.CharField(max_length=100, db_column='granted_by', blank=True)
    grant_date = models.DateField(db_column='grant_date', null=True, blank=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self.booking_id} - Venue {self.venue_id} ({self.event_date})"
    
    @property
    def venue(self):
        """Get venue object for backward compatibility"""
        try:
            return Venue.objects.get(venue_id=self.venue_id)
        except Venue.DoesNotExist:
            return None
    
    @property
    def user_id(self):
        """Alias for applicant_id for backward compatibility"""
        return str(self.applicant_id)
    
    @property
    def start_time_datetime(self):
        """Combine date and time for backward compatibility"""
        return timezone.datetime.combine(self.event_date, self.start_time)
    
    @property
    def end_time_datetime(self):
        """Combine date and time for backward compatibility"""
        return timezone.datetime.combine(self.event_date, self.end_time)
    
    @property
    def total_cost(self):
        """Calculate total cost based on venue rates"""
        venue = self.venue
        if not venue:
            return Decimal('0.00')
        
        hours = float(self.total_hours)
        if hours <= 2:
            return venue.base_rate_2h
        elif hours <= 4:
            return venue.base_rate_4h
        elif hours <= 6:
            return venue.base_rate_6h
        else:
            return venue.base_rate_6h_plus
    
    @property
    def notes(self):
        """Alias for event_details for backward compatibility"""
        return self.event_details