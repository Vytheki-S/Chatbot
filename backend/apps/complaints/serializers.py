from rest_framework import serializers
from .models import Complaint, ComplaintReply, ComplaintAttachment


class ComplaintAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintAttachment
        fields = ['attachment_id', 'complaint_id', 'file_name', 'file_path', 'uploaded_at']


class ComplaintReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintReply
        fields = ['reply_id', 'complaint_id', 'replied_by', 'reply_message', 'reply_attachment_name', 'reply_attachment_path', 'created_at']


class ComplaintSerializer(serializers.ModelSerializer):
    replies = ComplaintReplySerializer(many=True, read_only=True)
    attachments = ComplaintAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'complaint_id', 'user_id', 'subject', 'description', 
            'complaint_category', 'complaint_priority', 'complaint_status', 
            'created_at', 'updated_at', 'replies', 'attachments'
        ]
        read_only_fields = ['complaint_id', 'created_at', 'updated_at']


class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['user_id', 'subject', 'description', 'complaint_category', 'complaint_priority']


class ComplaintReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintReply
        fields = ['complaint_id', 'replied_by', 'reply_message', 'reply_attachment_name', 'reply_attachment_path']
