from django.contrib import admin
from .models import Timetable

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'faculty', 'day_of_week', 'start_time', 'end_time', 'room_number')
    list_filter = ('day_of_week', 'course', 'room_number')
    search_fields = ('course__name', 'faculty__user__username')
