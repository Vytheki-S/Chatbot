from django.urls import include, path
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chatbot/', include('apps.chatbot.urls')),
    path('api/booking/', include('apps.booking.urls')),
]