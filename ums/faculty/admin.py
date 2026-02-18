from django.contrib import admin
from .models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation', 'joining_date')
    search_fields = ('user__username', 'user__email', 'designation')
    list_filter = ('department', 'designation')
