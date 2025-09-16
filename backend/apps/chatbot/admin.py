from django.contrib import admin
from .models import ChatbotMessage

@admin.register(ChatbotMessage)
class ChatbotMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'user_id', 'sender_type', 'message_text', 'timestamp')
    list_filter = ('sender_type', 'timestamp')
    search_fields = ('user_id', 'message_text', 'response_text')
    readonly_fields = ('timestamp',)