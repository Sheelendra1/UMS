from django.contrib import admin
from .models import Exam, Result


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    raw_id_fields = ('student',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_type', 'total_marks', 'date')
    list_filter = ('exam_type', 'date')
    search_fields = ('course__name',)
    inlines = [ResultInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'marks_obtained')
    list_filter = ('exam__exam_type',)
    raw_id_fields = ('exam', 'student')
