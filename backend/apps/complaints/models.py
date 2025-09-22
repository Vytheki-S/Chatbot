from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Complaint(models.Model):
    COMPLAINT_CATEGORIES = [
        ('Technical Issue', 'Technical Issue'),
        ('Customer Service', 'Customer Service'),
        ('Payment Issue', 'Payment Issue'),
        ('Event Booking', 'Event Booking'),
        ('Service Quality', 'Service Quality'),
        ('Other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed'),
    ]
    
    complaint_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=1)  # Default user ID
    subject = models.CharField(max_length=255)
    description = models.TextField()
    complaint_category = models.CharField(max_length=50, choices=COMPLAINT_CATEGORIES, default='Other')
    complaint_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    complaint_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'complaints'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.complaint_status}"


class ComplaintReply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    complaint_id = models.IntegerField()
    replied_by = models.IntegerField(default=1)  # Default user ID
    reply_message = models.TextField()
    reply_attachment_name = models.CharField(max_length=255, blank=True, null=True)
    reply_attachment_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'complaint_replies'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply to complaint {self.complaint_id}"


class ComplaintAttachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    complaint_id = models.IntegerField()
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'complaint_attachments'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.file_name} - complaint {self.complaint_id}"
