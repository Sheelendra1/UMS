from django.contrib import admin
from .models import Attendance, AttendanceRecord

class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 1

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'course', 'marked_by')
    list_filter = ('date', 'course')
    inlines = [AttendanceRecordInline]

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'attendance', 'status')
    list_filter = ('status', 'attendance__date', 'attendance__course')
