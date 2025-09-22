from django.contrib import admin
from .models import (
    ChatSession, ChatMessage, ChatbotMessage, Applicant, Venue, VenueImage, 
    PriceTier, Booking, Feedback, BookingSlot, AdditionalService, PreArrangement,
    BookingService, NewPayment, OnlinePayment, ManualPayment, PaymentNotification,
    Refund, RefundBankDetails, PaymentAuditLog, PaymentInvoice, LegacyPayment,
    BankSlip, RefundRequest, JTCCHistory, JTCCFunder, JTCCFacility, JTCCMilestone, Contact
)

# Chat Models Admin
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user_id']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'sender_type', 'content_preview', 'created_at']
    list_filter = ['sender_type', 'created_at']
    search_fields = ['content', 'session__user_id']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(ChatbotMessage)
class ChatbotMessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'sender_type', 'user_id', 'message_preview', 'resolved', 'timestamp']
    list_filter = ['sender_type', 'resolved', 'timestamp']
    search_fields = ['message_text', 'response_text', 'booking_reference']
    
    def message_preview(self, obj):
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    message_preview.short_description = 'Message Preview'

# Venue Booking System Admin

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['applicant_id', 'applicant_name', 'organization', 'organization_type', 'email', 'contact_no']
    list_filter = ['organization_type']
    search_fields = ['applicant_name', 'organization', 'email']
    readonly_fields = ['applicant_id']

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['venue_id', 'venue_name', 'capacity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['venue_name', 'description']
    readonly_fields = ['venue_id', 'created_at']

@admin.register(VenueImage)
class VenueImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'venue', 'display_order', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['venue__venue_name']

@admin.register(PriceTier)
class PriceTierAdmin(admin.ModelAdmin):
    list_display = ['tier_id', 'venue', 'duration', 'price']
    list_filter = ['venue']
    search_fields = ['venue__venue_name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'booking_reference', 'applicant', 'total_amount', 'booking_status', 'payment_status', 'created_at']
    list_filter = ['booking_status', 'payment_status', 'is_public', 'created_at']
    search_fields = ['booking_reference', 'applicant__applicant_name', 'event_details']
    readonly_fields = ['booking_id', 'booking_reference', 'created_at', 'updated_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_id', 'booking', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['booking__booking_reference', 'user__username']

@admin.register(BookingSlot)
class BookingSlotAdmin(admin.ModelAdmin):
    list_display = ['slot_id', 'booking', 'venue', 'start_date', 'end_date', 'venue_cost', 'isfullday']
    list_filter = ['start_date', 'isfullday']
    search_fields = ['booking__booking_reference', 'venue__venue_name']

@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ['service_id', 'service_name', 'basic_rate', 'extra_hourly_rate', 'is_mandatory']
    list_filter = ['is_mandatory']
    search_fields = ['service_name']

@admin.register(PreArrangement)
class PreArrangementAdmin(admin.ModelAdmin):
    list_display = ['arrangement_id', 'booking', 'venue', 'arrangement_type', 'date', 'start_time', 'end_time']
    list_filter = ['arrangement_type', 'date']
    search_fields = ['booking__booking_reference', 'venue__venue_name']

@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ['booking_service_id', 'booking', 'service', 'duration_hours', 'service_cost']
    list_filter = ['service']
    search_fields = ['booking__booking_reference', 'service__service_name']

# Payment System Admin

@admin.register(NewPayment)
class NewPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'amount', 'currency', 'status', 'payment_type', 'created_at']
    list_filter = ['status', 'payment_type', 'created_at']
    search_fields = ['booking__booking_reference']
    readonly_fields = ['id', 'created_at']

@admin.register(OnlinePayment)
class OnlinePaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'payhere_payment_id', 'payhere_order_id']
    search_fields = ['payment__booking__booking_reference', 'payhere_payment_id', 'payhere_order_id']

@admin.register(ManualPayment)
class ManualPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'method', 'paid_date', 'verified_by']
    list_filter = ['method', 'paid_date']
    search_fields = ['payment__booking__booking_reference']

@admin.register(PaymentNotification)
class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'status', 'received_at']
    list_filter = ['status', 'received_at']
    search_fields = ['payment__booking__booking_reference']

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'refund_amount', 'status', 'requested_at', 'processed_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['payment__booking__booking_reference']

@admin.register(RefundBankDetails)
class RefundBankDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'refund', 'account_holder', 'bank_name', 'account_number']
    search_fields = ['account_holder', 'bank_name', 'account_number']

@admin.register(PaymentAuditLog)
class PaymentAuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'action', 'performed_by', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['payment__booking__booking_reference', 'performed_by']

@admin.register(PaymentInvoice)
class PaymentInvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'file_name', 'generated_at']
    list_filter = ['generated_at']
    search_fields = ['payment__booking__booking_reference', 'file_name']

@admin.register(LegacyPayment)
class LegacyPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'order_id', 'amount', 'status', 'gateway', 'created_at']
    list_filter = ['status', 'gateway', 'created_at']
    search_fields = ['booking__booking_reference', 'order_id']

@admin.register(BankSlip)
class BankSlipAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'original_filename', 'file_size', 'verified_by', 'uploaded_at']
    list_filter = ['stored_locally', 'stored_in_cloud', 'conversion_successful', 'uploaded_at']
    search_fields = ['payment__booking__booking_reference', 'original_filename']

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking_id', 'applicant_name', 'total_amount_paid', 'status', 'created_at']
    list_filter = ['status', 'event_type', 'venue_booked', 'created_at']
    search_fields = ['booking_id', 'applicant_name', 'organization_name']
    readonly_fields = ['id', 'created_at', 'updated_at']

# JTCC Information Admin

@admin.register(JTCCHistory)
class JTCCHistoryAdmin(admin.ModelAdmin):
    list_display = ['history_id', 'official_name', 'common_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['official_name', 'common_name', 'location']
    readonly_fields = ['history_id', 'created_at', 'updated_at']

@admin.register(JTCCFunder)
class JTCCFunderAdmin(admin.ModelAdmin):
    list_display = ['funder_id', 'funder_name', 'funder_type', 'country', 'is_active', 'created_at']
    list_filter = ['funder_type', 'is_active', 'created_at']
    search_fields = ['funder_name', 'country']

@admin.register(JTCCFacility)
class JTCCFacilityAdmin(admin.ModelAdmin):
    list_display = ['facility_id', 'facility_name', 'facility_type', 'capacity', 'is_available', 'created_at']
    list_filter = ['facility_type', 'is_available', 'created_at']
    search_fields = ['facility_name']

@admin.register(JTCCMilestone)
class JTCCMilestoneAdmin(admin.ModelAdmin):
    list_display = ['milestone_id', 'title', 'event_type', 'event_date', 'conducted_by', 'created_at']
    list_filter = ['event_type', 'event_date', 'created_at']
    search_fields = ['title', 'description', 'conducted_by']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'email', 'available_time']
    search_fields = ['phone_number', 'email']