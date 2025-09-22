from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import connection
from .models import Complaint, ComplaintReply, ComplaintAttachment
from .serializers import (
    ComplaintSerializer, ComplaintCreateSerializer, 
    ComplaintReplySerializer, ComplaintReplyCreateSerializer,
    ComplaintAttachmentSerializer
)


@api_view(['GET', 'POST'])
def get_complaints(request):
    """Get all complaints or create a new complaint"""
    if request.method == 'POST':
        # Handle complaint creation
        try:
            # Extract data from form data
            subject = request.data.get('title', '') or request.data.get('subject', '')
            description = request.data.get('description', '')
            complaint_category = request.data.get('complaint_category', 'Other')
            complaint_priority = request.data.get('complaint_priority', 'Low')
            user_id = request.data.get('user_id', 1)
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO complaints (user_id, subject, description, complaint_category, complaint_priority, complaint_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [user_id, subject, description, complaint_category, complaint_priority, 'Open'])
                complaint_id = cursor.lastrowid
            
            # Handle file uploads if any
            if 'files' in request.FILES:
                files = request.FILES.getlist('files')
                for file in files:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO complaint_attachments (complaint_id, file_name, file_path)
                            VALUES (%s, %s, %s)
                        """, [complaint_id, file.name, f"complaint_attachments/{complaint_id}/{file.name}"])
            
            return Response({'complaint_id': complaint_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle GET request - get all complaints
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.complaint_id, c.user_id, c.subject, c.description, 
                   c.complaint_category, c.complaint_priority, c.complaint_status,
                   c.created_at, c.updated_at
            FROM complaints c 
            ORDER BY c.created_at DESC
        """)
        columns = [col[0] for col in cursor.description]
        complaints = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Get replies for each complaint
    for complaint in complaints:
        complaint_id = complaint['complaint_id']
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT reply_id, complaint_id, replied_by, reply_message, 
                       reply_attachment_name, reply_attachment_path, created_at
                FROM complaint_replies 
                WHERE complaint_id = %s
                ORDER BY created_at ASC
            """, [complaint_id])
            reply_columns = [col[0] for col in cursor.description]
            complaint['replies'] = [dict(zip(reply_columns, row)) for row in cursor.fetchall()]
    
    # Get attachments for each complaint
    for complaint in complaints:
        complaint_id = complaint['complaint_id']
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT attachment_id, complaint_id, file_name, file_path, uploaded_at
                FROM complaint_attachments 
                WHERE complaint_id = %s
                ORDER BY uploaded_at DESC
            """, [complaint_id])
            attachment_columns = [col[0] for col in cursor.description]
            complaint['attachments'] = [dict(zip(attachment_columns, row)) for row in cursor.fetchall()]
    
    # Format response to match frontend expectations
    formatted_complaints = []
    for complaint in complaints:
        formatted_complaint = {
            'complaint_id': complaint['complaint_id'],
            'user': {
                'name': 'Anonymous',
                'email': 'anonymous@example.com',
                'role': 'Customer'
            },
            'subject': complaint['subject'],
            'description': complaint['description'],
            'complaint_category': complaint['complaint_category'],
            'complaint_priority': complaint['complaint_priority'],
            'complaint_status': complaint['complaint_status'],
            'created_at': complaint['created_at'].isoformat() + 'Z' if complaint['created_at'] else None,
            'updated_at': complaint['updated_at'].isoformat() + 'Z' if complaint['updated_at'] else None,
            'replies': complaint['replies'],
            'attachments': complaint['attachments'],
            'priority_color': 'text-green-600 bg-green-50' if complaint['complaint_priority'] == 'Low' else 'text-orange-600 bg-orange-50',
            'priority_icon': '📝' if complaint['complaint_priority'] == 'Low' else '⚠️',
            'id': complaint['complaint_id']
        }
        formatted_complaints.append(formatted_complaint)
    
    return Response({
        'results': formatted_complaints,
        'count': len(formatted_complaints),
        'next': False,
        'previous': False,
        'current_page': 1,
        'total_pages': 1
    })


@api_view(['POST'])
def create_complaint(request):
    """Create a new complaint"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO complaints (user_id, subject, description, complaint_category, complaint_priority, complaint_status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [
                request.data.get('user_id', 1),
                request.data.get('subject', ''),
                request.data.get('description', ''),
                request.data.get('complaint_category', 'Other'),
                request.data.get('complaint_priority', 'Low'),
                'Open'
            ])
            complaint_id = cursor.lastrowid
        
        return Response({'complaint_id': complaint_id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_replies(request):
    """Get all replies"""
    complaint_id = request.GET.get('complaint_id')
    if not complaint_id:
        return Response({'error': 'Complaint ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT reply_id, complaint_id, replied_by, reply_message, 
                   reply_attachment_name, reply_attachment_path, created_at
            FROM complaint_replies 
            WHERE complaint_id = %s
            ORDER BY created_at ASC
        """, [complaint_id])
        columns = [col[0] for col in cursor.description]
        replies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return Response(replies)


@api_view(['POST'])
def create_reply(request):
    """Create a new reply"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO complaint_replies (complaint_id, replied_by, reply_message, reply_attachment_name, reply_attachment_path)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                request.data.get('complaint_id'),
                request.data.get('replied_by', 1),
                request.data.get('reply_message', ''),
                request.data.get('reply_attachment_name', ''),
                request.data.get('reply_attachment_path', '')
            ])
            reply_id = cursor.lastrowid
        
        return Response({'reply_id': reply_id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_attachments(request):
    """Get all attachments"""
    complaint_id = request.GET.get('complaint_id')
    if not complaint_id:
        return Response({'error': 'Complaint ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT attachment_id, complaint_id, file_name, file_path, uploaded_at
            FROM complaint_attachments 
            WHERE complaint_id = %s
            ORDER BY uploaded_at DESC
        """, [complaint_id])
        columns = [col[0] for col in cursor.description]
        attachments = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return Response(attachments)


@api_view(['POST'])
def create_attachment(request):
    """Create a new attachment"""
    try:
        complaint_id = request.data.get('complaint_id')
        file_name = request.data.get('file_name', '')
        file_path = request.data.get('file_path', '')
        
        if not complaint_id:
            return Response({'error': 'complaint_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO complaint_attachments (complaint_id, file_name, file_path)
                VALUES (%s, %s, %s)
            """, [complaint_id, file_name, file_path])
            attachment_id = cursor.lastrowid
        
        return Response({'attachment_id': attachment_id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
