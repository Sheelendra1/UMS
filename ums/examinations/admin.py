from django.contrib import admin
from .models import Exam, Result

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_type', 'date', 'total_marks')
    list_filter = ('exam_type', 'date', 'course')
    inlines = [ResultInline]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained')
    search_fields = ('student__enrollment_no', 'exam__course__name')
    list_filter = ('exam',)
