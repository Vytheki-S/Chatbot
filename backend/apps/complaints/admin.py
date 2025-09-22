from django.contrib import admin
from .models import Complaint, ComplaintReply, ComplaintAttachment


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'subject', 'user_id', 'complaint_category', 'complaint_priority', 'complaint_status', 'created_at']
    list_filter = ['complaint_status', 'complaint_category', 'complaint_priority', 'created_at']
    search_fields = ['subject', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(ComplaintReply)
class ComplaintReplyAdmin(admin.ModelAdmin):
    list_display = ['reply_id', 'complaint_id', 'replied_by', 'reply_message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['reply_message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(ComplaintAttachment)
class ComplaintAttachmentAdmin(admin.ModelAdmin):
    list_display = ['attachment_id', 'complaint_id', 'file_name', 'file_path', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['file_name']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
