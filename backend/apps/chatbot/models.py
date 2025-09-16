from django.db import models
from django.utils import timezone


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


