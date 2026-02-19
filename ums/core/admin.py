from django.contrib import admin
from .models import UniversitySetting


@admin.register(UniversitySetting)
class UniversitySettingAdmin(admin.ModelAdmin):
    list_display = ('university_name', 'academic_year', 'current_semester')

    def has_add_permission(self, request):
        # Enforce singleton: only allow adding if none exists
        if UniversitySetting.objects.exists():
            return False
        return super().has_add_permission(request)
