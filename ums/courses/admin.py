from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'semester', 'credits')
    search_fields = ('code', 'name')
    list_filter = ('department', 'semester')
