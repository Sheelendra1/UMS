from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_no', 'user', 'department', 'semester', 'admission_date')
    list_filter = ('department', 'semester')
    search_fields = ('enrollment_no', 'user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)
