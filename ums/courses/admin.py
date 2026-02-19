from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'faculty', 'semester', 'credits')
    list_filter = ('department', 'semester')
    search_fields = ('name', 'code')
    raw_id_fields = ('faculty',)
    filter_horizontal = ('students',)
