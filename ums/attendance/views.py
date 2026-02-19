from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Attendance, AttendanceRecord
from courses.models import Course
from datetime import date

@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('course', 'marked_by').order_by('-date')
    
    # Determine user role and filter accordingly
    if hasattr(request.user, 'faculty'):
        faculty = request.user.faculty
        attendances = attendances.filter(course__faculty=faculty)
        courses = Course.objects.filter(faculty=faculty).order_by('name')
    elif hasattr(request.user, 'student'):
        # Students should probably use a different view or see their own records
        # For now, restrict list view to admin/faculty
        if not request.user.is_superuser:
             # Basic restriction
             attendances = attendances.none()
             courses = Course.objects.none()
        else:
            courses = Course.objects.all().order_by('name')
    else:
        # Admin or specific staff
        if not request.user.is_superuser and not request.user.is_staff:
             attendances = attendances.none()
             courses = Course.objects.none()
        else:
             courses = Course.objects.all().order_by('name')
    
    # Filter
    course_id = request.GET.get('course')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if course_id:
        attendances = attendances.filter(course_id=course_id)
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
    
    # Determine base template
    base_template = 'base.html'
    if hasattr(request.user, 'faculty'):
        base_template = 'teacher/base_teacher.html'
    elif hasattr(request.user, 'student'):
        base_template = 'student/base_student.html'

    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'courses': courses,
        'selected_course': int(course_id) if course_id and course_id.isdigit() else None,
        'start_date': start_date,
        'end_date': end_date,
        'base_template': base_template,
    })

@login_required
def attendance_detail(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    records = AttendanceRecord.objects.filter(attendance=attendance).select_related('student')
    
    total = records.count()
    present = records.filter(status=True).count()
    percentage = (present / total * 100) if total > 0 else 0

    # Determine base template
    base_template = 'base.html'
    if hasattr(request.user, 'faculty'):
        base_template = 'teacher/base_teacher.html'
    elif hasattr(request.user, 'student'):
        base_template = 'student/base_student.html'

    return render(request, 'attendance/attendance_detail.html', {
        'attendance': attendance,
        'records': records,
        'total': total,
        'present': present,
        'absent': total - present,
        'percentage': round(percentage, 2),
        'base_template': base_template,
    })

import csv
from django.http import HttpResponse

@login_required
def attendance_export(request):
    attendances = Attendance.objects.select_related('course', 'marked_by').order_by('-date')
    
    # Filter
    course_id = request.GET.get('course')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if course_id:
        attendances = attendances.filter(course_id=course_id)
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Course', 'Marked By'])
    
    for att in attendances:
        writer.writerow([
            att.date, 
            att.course.name, 
            att.marked_by.user.get_full_name() if att.marked_by else 'Unknown'
        ])
    
    return response
