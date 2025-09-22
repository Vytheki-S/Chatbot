from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ChatSession(models.Model):
    """Chat session model for grouping messages"""
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chatbot_sessions'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Session {self.id} - User {self.user_id}"


class ChatMessage(models.Model):
    """Chat message model for individual messages"""
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=20, choices=[
        ('user', 'User'),
        ('admin', 'Admin'),
        ('system', 'System'),
    ], default='user')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_messages_new'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender_type}: {self.content[:50]}..."


class ChatbotMessage(models.Model):
    """Chat message model matching existing chatbot_messages table."""
    SENDER_TYPE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('system', 'System'),
    ]
    
    message_id = models.AutoField(primary_key=True, db_column='message_id')
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES, default='user', db_column='sender_type')
    user_id = models.IntegerField(null=True, blank=True, db_column='user_id')
    message_text = models.TextField(db_column='message_text')
    response_text = models.TextField(null=True, blank=True, db_column='response_text')
    timestamp = models.DateTimeField(auto_now_add=True, db_column='timestamp')
    booking_reference = models.CharField(max_length=100, null=True, blank=True, db_column='booking_reference')
    resolved = models.BooleanField(default=False, db_column='resolved')
    
    class Meta:
        db_table = 'chatbot_messages'  # Match your existing table name
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender_type}: {self.message_text[:50]}..."


# New Models for Venue Booking System

class Applicant(models.Model):
    """Applicant model for venue booking"""
    ORGANIZATION_TYPE_CHOICES = [
        ('corporate_business', 'Corporate Business'),
        ('educational_institution', 'Educational Institution'),
        ('non_profit_ngo', 'Non-Profit/NGO'),
        ('government_public_sector', 'Government/Public Sector'),
        ('private_individual', 'Private Individual'),
        ('religious_organization', 'Religious Organization'),
        ('entertainment_event_management', 'Entertainment/Event Management'),
        ('other', 'Other'),
    ]
    
    applicant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant_profile')
    applicant_name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPE_CHOICES, default='other')
    organization = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    
    class Meta:
        db_table = 'chatbot_applicants'
    
    def __str__(self):
        return f"{self.applicant_name} - {self.organization}"


class Venue(models.Model):
    """Venue model for booking venues"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    venue_id = models.AutoField(primary_key=True)
    venue_name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    image = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_venues'
    
    def __str__(self):
        return f"{self.venue_name} (Capacity: {self.capacity})"


class VenueImage(models.Model):
    """Venue images model"""
    image_id = models.AutoField(primary_key=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=500)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_venue_images'
        ordering = ['display_order']
    
    def __str__(self):
        return f"Image for {self.venue.venue_name}"


class PriceTier(models.Model):
    """Price tiers for venues"""
    tier_id = models.AutoField(primary_key=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='price_tiers')
    duration = models.IntegerField()  # Duration in hours
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'chatbot_price_tiers'
    
    def __str__(self):
        return f"{self.venue.venue_name} - {self.duration}h - LKR {self.price}"


class Booking(models.Model):
    """Main booking model"""
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
    
    booking_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='bookings')
    booking_reference = models.CharField(max_length=20, unique=True)
    event_types = models.JSONField()  # List of event types
    custom_event_type = models.CharField(max_length=200, blank=True, null=True)
    event_details = models.TextField()
    additional_notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chatbot_bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self.booking_reference} - {self.applicant.applicant_name}"


class Feedback(models.Model):
    """Feedback model for bookings"""
    feedback_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_feedback'
    
    def __str__(self):
        return f"Feedback for {self.booking.booking_reference} - Rating: {self.rating}"


class BookingSlot(models.Model):
    """Booking slots for specific dates and times"""
    slot_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='slots')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    tier = models.ForeignKey(PriceTier, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue_cost = models.DecimalField(max_digits=10, decimal_places=2)
    isfullday = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'chatbot_booking_slots'
    
    def __str__(self):
        return f"Slot {self.slot_id} - {self.venue.venue_name} - {self.start_date}"


class AdditionalService(models.Model):
    """Additional services for bookings"""
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    basic_rate = models.DecimalField(max_digits=10, decimal_places=2)
    extra_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_mandatory = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'chatbot_additional_services'
    
    def __str__(self):
        return f"{self.service_name} - LKR {self.basic_rate}"


class PreArrangement(models.Model):
    """Pre-arrangements for bookings"""
    ARRANGEMENT_TYPE_CHOICES = [
        ('setup', 'Setup'),
        ('rehearsal', 'Rehearsal'),
        ('breakdown', 'Breakdown'),
    ]
    
    arrangement_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='pre_arrangements')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    arrangement_type = models.CharField(max_length=20, choices=ARRANGEMENT_TYPE_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'chatbot_pre_arrangements'
    
    def __str__(self):
        return f"{self.arrangement_type} - {self.venue.venue_name} - {self.date}"


class BookingService(models.Model):
    """Services associated with booking slots"""
    booking_service_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_services')
    slot = models.ForeignKey(BookingSlot, on_delete=models.CASCADE)
    service = models.ForeignKey(AdditionalService, on_delete=models.CASCADE)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'chatbot_booking_services'
    
    def __str__(self):
        return f"{self.service.service_name} - {self.slot.venue.venue_name}"


# Payment Models

class NewPayment(models.Model):
    """New payment model"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('online', 'Online'),
        ('manual', 'Manual'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='LKR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='online')
    
    class Meta:
        db_table = 'chatbot_new_payments'
        indexes = [
            models.Index(fields=['booking']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Payment {self.id} - {self.booking.booking_reference} - {self.amount} {self.currency}"


class OnlinePayment(models.Model):
    """Online payment details"""
    id = models.BigAutoField(primary_key=True)
    payment = models.OneToOneField(NewPayment, on_delete=models.CASCADE, related_name='online_payment')
    payhere_payment_id = models.CharField(max_length=100, default='')
    payhere_order_id = models.CharField(max_length=100, default='')
    payment_token = models.CharField(max_length=255, default='')
    authorization_token = models.CharField(max_length=500, default='')
    md5_signature = models.CharField(max_length=32, default='')
    
    class Meta:
        db_table = 'chatbot_online_payments'
        indexes = [
            models.Index(fields=['payhere_payment_id']),
            models.Index(fields=['payhere_order_id']),
        ]
    
    def __str__(self):
        return f"Online Payment {self.id} - {self.payment.booking.booking_reference}"


class ManualPayment(models.Model):
    """Manual payment details"""
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('bank_slip', 'Bank Slip'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    payment = models.OneToOneField(NewPayment, on_delete=models.CASCADE, related_name='manual_payment')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    paid_date = models.DateField()
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.CharField(max_length=255, default='')
    
    class Meta:
        db_table = 'chatbot_manual_payments'
        indexes = [
            models.Index(fields=['method']),
            models.Index(fields=['paid_date']),
        ]
    
    def __str__(self):
        return f"Manual Payment {self.id} - {self.method} - {self.paid_date}"


class PaymentNotification(models.Model):
    """Payment notifications"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    payment = models.ForeignKey(NewPayment, on_delete=models.CASCADE, related_name='notifications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.TextField()
    raw_response = models.JSONField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_payment_notifications'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['received_at']),
        ]
    
    def __str__(self):
        return f"Notification {self.id} - {self.payment.booking.booking_reference} - {self.status}"


class Refund(models.Model):
    """Refund model"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    payment = models.ForeignKey(NewPayment, on_delete=models.CASCADE, related_name='refunds')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_reason = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'chatbot_refunds'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['requested_at']),
        ]
    
    def __str__(self):
        return f"Refund {self.id} - {self.payment.booking.booking_reference} - {self.refund_amount}"


class RefundBankDetails(models.Model):
    """Refund bank details"""
    id = models.BigAutoField(primary_key=True)
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name='bank_details')
    account_holder = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=50, default='')
    account_number = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=50, default='')
    
    class Meta:
        db_table = 'chatbot_refund_bank_details'
        indexes = [
            models.Index(fields=['bank_name']),
        ]
    
    def __str__(self):
        return f"Bank Details for Refund {self.refund.id} - {self.account_holder}"


class PaymentAuditLog(models.Model):
    """Payment audit logs"""
    id = models.BigAutoField(primary_key=True)
    payment = models.ForeignKey(NewPayment, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    performed_by = models.CharField(max_length=100)
    details = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_payment_audit_logs'
        indexes = [
            models.Index(fields=['action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Audit Log {self.id} - {self.action} - {self.performed_by}"


class PaymentInvoice(models.Model):
    """Payment invoices"""
    id = models.BigAutoField(primary_key=True)
    payment = models.ForeignKey(NewPayment, on_delete=models.CASCADE, related_name='invoices')
    cloudinary_public_id = models.CharField(max_length=255)
    cloudinary_url = models.CharField(max_length=500)
    file_name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_payment_invoices'
        indexes = [
            models.Index(fields=['cloudinary_public_id']),
            models.Index(fields=['generated_at']),
        ]
    
    def __str__(self):
        return f"Invoice {self.id} - {self.payment.booking.booking_reference}"


class LegacyPayment(models.Model):
    """Legacy payment model for migration"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('manual_pending', 'Manual Pending'),
        ('manual_verified', 'Manual Verified'),
        ('manual_rejected', 'Manual Rejected'),
    ]
    
    GATEWAY_CHOICES = [
        ('payhere', 'PayHere'),
        ('manual', 'Manual'),
    ]
    
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='legacy_payments')
    order_id = models.CharField(max_length=64, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='LKR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES, default='payhere')
    payment_method = models.CharField(max_length=20, default='card')
    gateway_payment_id = models.CharField(max_length=128, default='')
    raw_notification = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chatbot_legacy_payments'
        indexes = [
            models.Index(fields=['booking']),
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Legacy Payment {self.id} - {self.order_id} - {self.amount}"


class BankSlip(models.Model):
    """Bank slip model"""
    id = models.BigAutoField(primary_key=True)
    payment = models.OneToOneField(NewPayment, on_delete=models.CASCADE, related_name='bank_slip')
    file_path = models.CharField(max_length=500)
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField()
    file_type = models.CharField(max_length=50)
    cloudinary_url = models.CharField(max_length=500, null=True, blank=True)
    cloudinary_public_id = models.CharField(max_length=255, null=True, blank=True)
    stored_locally = models.BooleanField(default=True)
    stored_in_cloud = models.BooleanField(default=False)
    original_file_type = models.CharField(max_length=50, default='')
    converted_file_type = models.CharField(max_length=50, default='')
    conversion_successful = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True, null=True)
    verified_by = models.CharField(max_length=100, default='')
    verified_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_bank_slips'
        indexes = [
            models.Index(fields=['uploaded_at']),
        ]
    
    def __str__(self):
        return f"Bank Slip {self.id} - {self.payment.booking.booking_reference}"


class RefundRequest(models.Model):
    """Refund request model"""
    EVENT_TYPE_CHOICES = [
        ('cultural', 'Cultural'),
        ('conference', 'Conference'),
        ('exhibition', 'Exhibition'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('other', 'Other'),
    ]
    
    VENUE_CHOICES = [
        ('auditorium', 'Auditorium'),
        ('amphitheatre', 'Amphitheatre'),
        ('conference_hall', 'Conference Hall'),
        ('meeting_room', 'Meeting Room'),
        ('exhibition_hall', 'Exhibition Hall'),
        ('other', 'Other'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
        ('payhere', 'PayHere'),
        ('manual', 'Manual'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    booking_id = models.CharField(max_length=50, unique=True)
    applicant_name = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=200, default='')
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=100)
    event_date = models.DateField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    venue_booked = models.CharField(max_length=20, choices=VENUE_CHOICES)
    venue_other = models.CharField(max_length=100, default='')
    total_amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_receipt_number = models.CharField(max_length=100)
    payment_date = models.DateField()
    cancellation_reason = models.TextField()
    cancellation_request_date = models.DateField()
    expected_refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    refund_percentage = models.IntegerField(default=0)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=20)
    account_number = models.CharField(max_length=50)
    swift_code = models.CharField(max_length=20, default='')
    terms_acknowledged = models.BooleanField(default=False)
    digital_signature = models.TextField(blank=True, null=True)
    signature_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    processed_by = models.CharField(max_length=100, default='')
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chatbot_refund_requests'
        indexes = [
            models.Index(fields=['booking_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Refund Request {self.id} - {self.booking_id} - {self.applicant_name}"


# JTCC History and Information Models

class JTCCHistory(models.Model):
    """JTCC history model"""
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Maintenance', 'Under Maintenance'),
    ]
    
    history_id = models.AutoField(primary_key=True)
    official_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, default='JTCC')
    location = models.CharField(max_length=255)
    inauguration_date = models.DateField()
    inaugurated_by = models.CharField(max_length=255)
    description = models.TextField()
    facilities = models.TextField()
    renaming_date = models.DateField(null=True, blank=True)
    renaming_announced_by = models.CharField(max_length=255, blank=True, null=True)
    renaming_occasion = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chatbot_jtcc_history'
    
    def __str__(self):
        return f"{self.official_name} - {self.status}"


class JTCCFunder(models.Model):
    """JTCC funders model"""
    FUNDER_TYPE_CHOICES = [
        ('Government', 'Government'),
        ('Organization', 'Organization'),
        ('Individual', 'Individual'),
    ]
    
    funder_id = models.AutoField(primary_key=True)
    funder_name = models.CharField(max_length=255)
    funder_type = models.CharField(max_length=20, choices=FUNDER_TYPE_CHOICES)
    country = models.CharField(max_length=100, blank=True, null=True)
    role_description = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_jtcc_funders'
    
    def __str__(self):
        return f"{self.funder_name} - {self.funder_type}"


class JTCCFacility(models.Model):
    """JTCC facilities model"""
    FACILITY_TYPE_CHOICES = [
        ('Auditorium', 'Auditorium'),
        ('Conference Hall', 'Conference Hall'),
        ('Amphitheatre', 'Amphitheatre'),
        ('Library', 'Library'),
        ('Exhibition Space', 'Exhibition Space'),
        ('Open Space', 'Open Space'),
    ]
    
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES)
    capacity = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_jtcc_facilities'
    
    def __str__(self):
        return f"{self.facility_name} - {self.facility_type}"


class JTCCMilestone(models.Model):
    """JTCC milestones model"""
    EVENT_TYPE_CHOICES = [
        ('Inauguration', 'Inauguration'),
        ('Renaming', 'Renaming'),
        ('Cultural Event', 'Cultural Event'),
        ('Maintenance', 'Maintenance'),
        ('Expansion', 'Expansion'),
        ('Award', 'Award'),
    ]
    
    milestone_id = models.AutoField(primary_key=True)
    event_date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    conducted_by = models.CharField(max_length=255, blank=True, null=True)
    attendees = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_jtcc_milestones'
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"


class Contact(models.Model):
    """Contact information model"""
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    available_time = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'chatbot_contacts'
    
    def __str__(self):
        return f"Contact {self.id} - {self.phone_number or self.email}"


