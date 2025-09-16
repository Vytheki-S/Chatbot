from rest_framework import serializers
from .models import ChatbotMessage

class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = ['message_id', 'sender_type', 'user_id', 'message_text', 'response_text', 'timestamp', 'booking_reference', 'resolved']