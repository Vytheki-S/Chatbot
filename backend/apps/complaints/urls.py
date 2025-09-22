from django.urls import path
from . import views

urlpatterns = [
    # Complaints endpoints
    path('complaints/', views.get_complaints, name='complaints-list'),
    path('complaints/create/', views.create_complaint, name='complaints-create'),
    
    # Replies endpoints
    path('replies/', views.get_replies, name='replies-list'),
    path('replies/create/', views.create_reply, name='replies-create'),
    
    # Attachments endpoints
    path('attachments/', views.get_attachments, name='attachments-list'),
    path('attachments/create/', views.create_attachment, name='attachments-create'),
]
