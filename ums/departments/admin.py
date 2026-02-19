from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'hod')
    search_fields = ('name', 'code')
    raw_id_fields = ('hod',)
