# Temporarily disabled admin to check database structure
# from django.contrib import admin
# from .models import Venue, Booking, BookingDetail, BookingService

# @admin.register(Venue)
# class VenueAdmin(admin.ModelAdmin):
#     list_display = ('name', 'capacity', 'hourly_rate', 'is_available', 'created_at')
#     list_filter = ('is_available', 'capacity', 'created_at')
#     search_fields = ('name', 'description')
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'venue', 'user_id', 'start_time', 'end_time', 'total_cost', 'status')
#     list_filter = ('status', 'start_time', 'venue')
#     search_fields = ('user_id', 'venue__name')
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(BookingDetail)
# class BookingDetailAdmin(admin.ModelAdmin):
#     list_display = ('id', 'booking', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('booking__id',)
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(BookingService)
# class BookingServiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'booking', 'service_name', 'service_cost', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('service_name', 'booking__id')
#     readonly_fields = ('created_at',)
