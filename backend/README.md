# Chatbot Backend

A Django-based backend for an AI-powered venue booking chatbot system.

## Features

- **AI Chatbot**: Powered by OpenRouter API for intelligent venue recommendations
- **Venue Management**: CRUD operations for venues with availability tracking
- **Booking System**: Complete booking management with conflict detection
- **RESTful API**: Clean, documented API endpoints
- **Session Management**: Chat session tracking and history
- **Admin Interface**: Django admin for easy data management

## Project Structure

```
backend/
├── .env                          # Environment variables (NOT in version control)
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── config/                      # Project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI configuration
├── apps/
│   ├── __init__.py
│   ├── chatbot/                 # Chatbot application
│   │   ├── __init__.py
│   │   ├── admin.py             # Admin interface
│   │   ├── apps.py              # App configuration
│   │   ├── models.py            # Database models
│   │   ├── serializers.py       # API serializers
│   │   ├── services.py          # OpenRouter service
│   │   ├── views.py             # API views
│   │   ├── urls.py              # App URL routing
│   │   └── management/
│   │       └── commands/
│   │           ├── __init__.py
│   │           └── initialize_chatbot.py  # Data initialization
│   └── booking/                 # Booking application
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── management/
│           └── commands/
│               ├── __init__.py
│               └── initialize_venue_data.py
└── static/                      # Static files
└── templates/                   # HTML templates (if needed)
```

## Setup Instructions

### 1. Environment Setup

Create a `.env` file in the backend directory:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# OpenRouter API
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Initialize Sample Data

```bash
python manage.py initialize_chatbot
python manage.py initialize_venue_data
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Chatbot Endpoints

- `POST /api/chatbot/chat/` - Send chat message
- `GET /api/chatbot/sessions/{user_id}/` - Get user chat sessions
- `DELETE /api/chatbot/sessions/delete/{session_id}/` - Delete chat session
- `GET /api/chatbot/venues/` - Get available venues
- `POST /api/chatbot/venues/recommendations/` - Get AI venue recommendations
- `GET /api/chatbot/health/` - Health check

### Booking Endpoints

- `GET /api/booking/venues/` - Get all venues
- `POST /api/booking/venues/` - Create new venue
- `GET /api/booking/venues/{venue_id}/` - Get specific venue
- `PUT /api/booking/venues/{venue_id}/` - Update venue
- `DELETE /api/booking/venues/{venue_id}/` - Delete venue
- `GET /api/booking/venues/{venue_id}/availability/` - Check venue availability
- `GET /api/booking/bookings/` - Get all bookings
- `POST /api/booking/bookings/` - Create new booking
- `GET /api/booking/bookings/{booking_id}/` - Get specific booking
- `PUT /api/booking/bookings/{booking_id}/` - Update booking
- `DELETE /api/booking/bookings/{booking_id}/` - Cancel booking
- `GET /api/booking/users/{user_id}/bookings/` - Get user bookings

## Models

### Chatbot App

- **ChatSession**: Tracks chat conversations
- **ChatMessage**: Individual messages within sessions
- **Venue**: Venue information for recommendations

### Booking App

- **Venue**: Venue details and availability
- **Booking**: Reservation records with status tracking

## Services

### OpenRouterService

Handles communication with OpenRouter API for AI chat functionality.

### ChatService

Manages chat sessions, messages, and AI interactions.

## Management Commands

- `initialize_chatbot`: Sets up initial chatbot data
- `initialize_venue_data`: Creates sample venues for the booking system

## Configuration

The project uses `python-decouple` for environment variable management. Key settings include:

- Database configuration
- OpenRouter API credentials
- CORS settings
- Logging configuration
- REST Framework settings

## Development

### Adding New Features

1. Create models in the appropriate app
2. Add serializers for API responses
3. Implement views with proper error handling
4. Add URL patterns
5. Update admin interface if needed
6. Add tests

### Code Style

- Follow PEP 8 guidelines
- Use docstrings for all functions and classes
- Implement proper error handling
- Use Django best practices

## Deployment

### Production Settings

1. Set `DEBUG=False`
2. Configure production database
3. Set secure `SECRET_KEY`
4. Configure proper `ALLOWED_HOSTS`
5. Set up static file serving
6. Configure logging

### Environment Variables

Ensure all sensitive information is stored in environment variables and not committed to version control.

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository.
