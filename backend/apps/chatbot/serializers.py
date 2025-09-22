from rest_framework import serializers
from .models import (
    ChatSession, ChatMessage, ChatbotMessage, Applicant, Venue, VenueImage, 
    PriceTier, Booking, Feedback, BookingSlot, AdditionalService, PreArrangement,
    BookingService, NewPayment, OnlinePayment, ManualPayment, PaymentNotification,
    Refund, RefundBankDetails, PaymentAuditLog, PaymentInvoice, LegacyPayment,
    BankSlip, RefundRequest, JTCCHistory, JTCCFunder, JTCCFacility, JTCCMilestone, Contact
)

# Chat Models Serializers
class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'user_id', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'sender_type', 'content', 'created_at']

class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = ['message_id', 'sender_type', 'user_id', 'message_text', 'response_text', 'timestamp', 'booking_reference', 'resolved']

# Venue Booking System Serializers

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['applicant_id', 'user', 'applicant_name', 'organization_type', 'organization', 'contact_no', 'email']

class VenueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueImage
        fields = ['image_id', 'venue', 'image_url', 'display_order', 'uploaded_at']

class VenueSerializer(serializers.ModelSerializer):
    images = VenueImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venue
        fields = ['venue_id', 'venue_name', 'capacity', 'status', 'image', 'description', 'created_at', 'images']

class PriceTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceTier
        fields = ['tier_id', 'venue', 'duration', 'price']

class BookingSlotSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.venue_name', read_only=True)
    
    class Meta:
        model = BookingSlot
        fields = ['slot_id', 'booking', 'venue', 'venue_name', 'tier', 'start_date', 'end_date', 'start_time', 'end_time', 'venue_cost', 'isfullday']

class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = ['service_id', 'service_name', 'basic_rate', 'extra_hourly_rate', 'is_mandatory']

class PreArrangementSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.venue_name', read_only=True)
    
    class Meta:
        model = PreArrangement
        fields = ['arrangement_id', 'booking', 'venue', 'venue_name', 'arrangement_type', 'date', 'start_time', 'end_time', 'notes']

class BookingServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.service_name', read_only=True)
    
    class Meta:
        model = BookingService
        fields = ['booking_service_id', 'booking', 'slot', 'service', 'service_name', 'duration_hours', 'service_cost']

class BookingSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.applicant_name', read_only=True)
    slots = BookingSlotSerializer(many=True, read_only=True)
    pre_arrangements = PreArrangementSerializer(many=True, read_only=True)
    booking_services = BookingServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'applicant', 'applicant_name', 'booking_reference', 'event_types', 
            'custom_event_type', 'event_details', 'additional_notes', 'total_amount', 
            'booking_status', 'payment_status', 'is_public', 'created_at', 'updated_at',
            'slots', 'pre_arrangements', 'booking_services'
        ]

class FeedbackSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='booking.booking_reference', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['feedback_id', 'booking', 'booking_reference', 'user', 'rating', 'comment', 'created_at']

# Payment System Serializers

class NewPaymentSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='booking.booking_reference', read_only=True)
    
    class Meta:
        model = NewPayment
        fields = ['id', 'user', 'booking', 'booking_reference', 'amount', 'currency', 'status', 'created_at', 'payment_type']

class OnlinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlinePayment
        fields = ['id', 'payment', 'payhere_payment_id', 'payhere_order_id', 'payment_token', 'authorization_token', 'md5_signature']

class ManualPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualPayment
        fields = ['id', 'payment', 'method', 'paid_date', 'verified_by', 'notes']

class PaymentNotificationSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='payment.booking.booking_reference', read_only=True)
    
    class Meta:
        model = PaymentNotification
        fields = ['id', 'payment', 'booking_reference', 'status', 'message', 'raw_response', 'received_at']

class RefundSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='payment.booking.booking_reference', read_only=True)
    
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'booking_reference', 'refund_amount', 'refund_reason', 'status', 'requested_at', 'processed_at', 'processed_by']

class RefundBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundBankDetails
        fields = ['id', 'refund', 'account_holder', 'bank_name', 'branch_code', 'account_number', 'swift_code']

class PaymentAuditLogSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='payment.booking.booking_reference', read_only=True)
    
    class Meta:
        model = PaymentAuditLog
        fields = ['id', 'payment', 'booking_reference', 'action', 'performed_by', 'details', 'created_at']

class PaymentInvoiceSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='payment.booking.booking_reference', read_only=True)
    
    class Meta:
        model = PaymentInvoice
        fields = ['id', 'payment', 'booking_reference', 'cloudinary_public_id', 'cloudinary_url', 'file_name', 'image_filename', 'generated_at']

class LegacyPaymentSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='booking.booking_reference', read_only=True)
    
    class Meta:
        model = LegacyPayment
        fields = ['id', 'booking', 'booking_reference', 'order_id', 'amount', 'currency', 'status', 'gateway', 'payment_method', 'gateway_payment_id', 'raw_notification', 'created_at', 'updated_at']

class BankSlipSerializer(serializers.ModelSerializer):
    booking_reference = serializers.CharField(source='payment.booking.booking_reference', read_only=True)
    
    class Meta:
        model = BankSlip
        fields = ['id', 'payment', 'booking_reference', 'file_path', 'original_filename', 'file_size', 'file_type', 'cloudinary_url', 'cloudinary_public_id', 'stored_locally', 'stored_in_cloud', 'original_file_type', 'converted_file_type', 'conversion_successful', 'verification_notes', 'verified_by', 'verified_at', 'uploaded_at']

class RefundRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRequest
        fields = [
            'id', 'booking_id', 'applicant_name', 'organization_name', 'contact_phone', 
            'contact_email', 'event_date', 'event_type', 'venue_booked', 'venue_other',
            'total_amount_paid', 'payment_method', 'transaction_receipt_number', 'payment_date',
            'cancellation_reason', 'cancellation_request_date', 'expected_refund_amount',
            'refund_percentage', 'account_holder_name', 'bank_name', 'branch_code',
            'account_number', 'swift_code', 'terms_acknowledged', 'digital_signature',
            'signature_date', 'status', 'admin_notes', 'processed_by', 'processed_at',
            'created_at', 'updated_at'
        ]

# JTCC Information Serializers

class JTCCHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JTCCHistory
        fields = [
            'history_id', 'official_name', 'common_name', 'location', 'inauguration_date',
            'inaugurated_by', 'description', 'facilities', 'renaming_date', 'renaming_announced_by',
            'renaming_occasion', 'status', 'created_at', 'updated_at'
        ]

class JTCCFunderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JTCCFunder
        fields = ['funder_id', 'funder_name', 'funder_type', 'country', 'role_description', 'contact_info', 'is_active', 'created_at']

class JTCCFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JTCCFacility
        fields = ['facility_id', 'facility_name', 'facility_type', 'capacity', 'description', 'specifications', 'is_available', 'created_at']

class JTCCMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = JTCCMilestone
        fields = ['milestone_id', 'event_date', 'title', 'description', 'event_type', 'conducted_by', 'attendees', 'created_at']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone_number', 'email', 'available_time']

# Comprehensive Serializers for Complex Data

class VenueDetailSerializer(serializers.ModelSerializer):
    images = VenueImageSerializer(many=True, read_only=True)
    price_tiers = PriceTierSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venue
        fields = ['venue_id', 'venue_name', 'capacity', 'status', 'image', 'description', 'created_at', 'images', 'price_tiers']

class BookingDetailSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.applicant_name', read_only=True)
    applicant_organization = serializers.CharField(source='applicant.organization', read_only=True)
    slots = BookingSlotSerializer(many=True, read_only=True)
    pre_arrangements = PreArrangementSerializer(many=True, read_only=True)
    booking_services = BookingServiceSerializer(many=True, read_only=True)
    payments = NewPaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'applicant', 'applicant_name', 'applicant_organization', 'booking_reference',
            'event_types', 'custom_event_type', 'event_details', 'additional_notes', 'total_amount',
            'booking_status', 'payment_status', 'is_public', 'created_at', 'updated_at',
            'slots', 'pre_arrangements', 'booking_services', 'payments'
        ]