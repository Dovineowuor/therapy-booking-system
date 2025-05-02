from django.contrib import admin
from .models import TherapyService, Therapist, TimeSlot, Booking, Review

@admin.register(TherapyService)
class TherapyServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'specialization', 'experience_years')
    list_filter = ('specialization',)
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    filter_horizontal = ('services',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available', 'therapist')
    search_fields = ('therapist__user__first_name', 'therapist__user__last_name')
    date_hierarchy = 'date'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'therapist', 'service', 'get_date', 'get_time', 'status')
    list_filter = ('status', 'time_slot__date', 'service')
    search_fields = ('client__username', 'therapist__user__first_name', 'therapist__user__last_name')
    date_hierarchy = 'time_slot__date'
    
    def get_date(self, obj):
        return obj.time_slot.date
    get_date.short_description = 'Date'
    
    def get_time(self, obj):
        return f"{obj.time_slot.start_time} - {obj.time_slot.end_time}"
    get_time.short_description = 'Time'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('booking__client__username', 'comment')
