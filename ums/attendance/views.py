from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Attendance, AttendanceRecord
from courses.models import Course
from datetime import date

@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('course', 'marked_by').order_by('-date')
    courses = Course.objects.all()
    
    # Filter
    course_id = request.GET.get('course')
    filter_date = request.GET.get('date')

    if course_id:
        attendances = attendances.filter(course_id=course_id)
    if filter_date:
        attendances = attendances.filter(date=filter_date)

    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'courses': courses,
        'selected_course': int(course_id) if course_id else None,
        'selected_date': filter_date
    })

@login_required
def attendance_detail(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    records = AttendanceRecord.objects.filter(attendance=attendance).select_related('student')
    
    total = records.count()
    present = records.filter(status=True).count()
    percentage = (present / total * 100) if total > 0 else 0

    return render(request, 'attendance/attendance_detail.html', {
        'attendance': attendance,
        'records': records,
        'total': total,
        'present': present,
        'absent': total - present,
        'percentage': round(percentage, 2)
    })
