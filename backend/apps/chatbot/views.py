from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from .models import ChatbotMessage
from .services import OpenRouterService
from apps.booking.models import Venue, Booking
import json
from datetime import datetime, timedelta

def convert_user_id(user_id):
    """Convert user_id from string format to integer"""
    try:
        if isinstance(user_id, str):
            if user_id.startswith('user-'):
                return int(user_id.replace('user-', ''))
            else:
                return int(user_id)
        return int(user_id)
    except (ValueError, TypeError):
        return 1  # Default to user 1 if conversion fails

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """Get CSRF token for frontend"""
    return Response({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_chat_sessions(request, user_id):
    """Get all chat sessions for a specific user"""
    try:
        # Convert user_id from string to integer
        user_id_int = convert_user_id(user_id)
        
        # Get recent messages for the user (last 50 messages)
        messages = ChatbotMessage.objects.filter(
            user_id=user_id_int
        ).order_by('-timestamp')[:50]
        
        # Group messages by session (using timestamp grouping for simplicity)
        sessions = []
        current_session = []
        last_timestamp = None
        session_counter = 1
        
        for message in messages:
            # Start new session if more than 30 minutes gap or first message
            if last_timestamp is None or (last_timestamp - message.timestamp).total_seconds() > 1800:  # 30 minutes gap
                if current_session:
                    sessions.append({
                        'id': session_counter,
                        'user_id': user_id,
                        'messages': current_session,
                        'created_at': current_session[-1]['timestamp'],
                        'updated_at': current_session[0]['timestamp']
                    })
                    session_counter += 1
                current_session = []
            
            current_session.insert(0, {
                'message_id': message.message_id,
                'sender_type': message.sender_type,
                'user_id': message.user_id,
                'message_text': message.message_text,
                'response_text': message.response_text,
                'timestamp': message.timestamp.isoformat(),
                'booking_reference': message.booking_reference,
                'resolved': message.resolved
            })
            last_timestamp = message.timestamp
        
        # Add the last session
        if current_session:
            sessions.append({
                'id': session_counter,
                'user_id': user_id,
                'messages': current_session,
                'created_at': current_session[-1]['timestamp'],
                'updated_at': current_session[0]['timestamp']
            })
        
        return Response(sessions)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve sessions: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def send_message(request):
    """Send a message to the chatbot and get a response"""
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        user_id = data.get('user_id', 'user-123')  # Default user ID
        
        if not message_content:
            return Response(
                {'error': 'Message is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert user_id to integer
        user_id_int = convert_user_id(user_id)
        
        # Save user message
        user_message = ChatbotMessage.objects.create(
            sender_type='user',
            user_id=user_id_int,
            message_text=message_content,
            timestamp=datetime.now()
        )
        
        # Get response from OpenRouter with database context
        openrouter_service = OpenRouterService()
        bot_response = openrouter_service.generate_response(message_content)
        
        # Save bot response
        bot_message = ChatbotMessage.objects.create(
            sender_type='admin',
            user_id=user_id_int,
            message_text='',
            response_text=bot_response,
            timestamp=datetime.now()
        )
        
        return Response({
            'session_id': 1,  # Simplified for now
            'message_id': bot_message.message_id,
            'response': bot_response
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venues(request):
    """Get all available venues"""
    try:
        venues = Venue.objects.filter(is_available=True)
        venue_data = []
        
        for venue in venues:
            venue_data.append({
                'id': venue.id,
                'name': venue.name,
                'description': venue.description,
                'capacity': venue.capacity,
                'hourly_rate': float(venue.hourly_rate),
                'is_available': venue.is_available,
                'created_at': venue.created_at.isoformat(),
                'updated_at': venue.updated_at.isoformat()
            })
        
        return Response(venue_data)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to retrieve venues: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_venue_recommendations(request):
    """Get venue recommendations based on user message"""
    try:
        message = request.GET.get('message', '')
        if not message:
            return Response(
                {'error': 'Message parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use OpenRouter service to get recommendations
        openrouter_service = OpenRouterService()
        recommendations = openrouter_service.generate_response(message)
        
        return Response({
            'recommendations': recommendations
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to get recommendations: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    try:
        # Test database connection
        venue_count = Venue.objects.count()
        message_count = ChatbotMessage.objects.count()
        
        return Response({
            'status': 'healthy',
            'database': 'connected',
            'venues_count': venue_count,
            'messages_count': message_count
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_chat_session(request, session_id):
    """Delete a chat session (simplified - delete recent messages)"""
    try:
        # For simplicity, we'll delete messages older than 1 hour
        cutoff_time = datetime.now() - timedelta(hours=1)
        deleted_count = ChatbotMessage.objects.filter(
            timestamp__lt=cutoff_time
        ).delete()[0]
        
        return Response({
            'message': f'Deleted {deleted_count} old messages',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to delete session: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )