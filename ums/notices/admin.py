from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_audience', 'posted_by', 'created_at')
    list_filter = ('target_audience', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('posted_by', 'target_course')
