from django.contrib import admin
from .models import Attendance, AttendanceRecord


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0
    raw_id_fields = ('student',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'marked_by')
    list_filter = ('course', 'date')
    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'student', 'status')
    list_filter = ('status',)
    raw_id_fields = ('attendance', 'student')
