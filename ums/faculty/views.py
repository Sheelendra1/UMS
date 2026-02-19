from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Max, Min, Count, Q
from decimal import Decimal
import calendar

from .models import Faculty
from departments.models import Department
from accounts.models import CustomUser
from courses.models import Course
from students.models import Student
from attendance.models import Attendance, AttendanceRecord
from examinations.models import Exam, Result
from notices.models import Notice
from timetable.models import Timetable
from django.contrib.auth.hashers import make_password
import random
import string


# ── Helper ───────────────────────────────────────────────────────────────────
def faculty_required(view_func):
    """Decorator: user must be logged-in AND be a Faculty member."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'faculty'):
            messages.error(request, 'Access denied. Faculty account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


# ── Admin-facing views (unchanged) ──────────────────────────────────────────
@login_required
def faculty_list(request):
    dept_id = request.GET.get('department')
    search_query = request.GET.get('q')

    faculty_members = Faculty.objects.select_related('user', 'department').all()

    if dept_id:
        faculty_members = faculty_members.filter(department_id=dept_id)
    if search_query:
        faculty_members = faculty_members.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    departments = Department.objects.all()
    
    return render(request, 'faculty/faculty_list.html', {
        'faculty_members': faculty_members,
        'departments': departments,
        'selected_dept': int(dept_id) if dept_id and dept_id.isdigit() else None,
        'search_query': search_query
    })


@login_required
def add_faculty(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = request.POST.get('username') # Not present in form
        dept_id = request.POST.get('department')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')
        password = request.POST.get('password')
        auto_gen = request.POST.get('auto_generate')

        if auto_gen or not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Generate Username
        base_username = f"{first_name.lower()}.{last_name.lower()}"
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=CustomUser.Role.FACULTY
            )
            if request.FILES.get('profile_image'):
                user.profile_image = request.FILES['profile_image']
            user.set_password(password)
            user.save()

            dept = Department.objects.get(id=dept_id)
            Faculty.objects.create(
                user=user,
                department=dept,
                designation=designation,
                joining_date=joining_date
            )
            messages.success(request, f'Faculty added. Password: {password}')
            return redirect('faculty_list')
        except Exception as e:
            messages.error(request, f'Error adding faculty: {e}')

    departments = Department.objects.all()
    return render(request, 'faculty/add_faculty.html', {'departments': departments})


@login_required
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    # Get courses assigned to this faculty
    courses = Course.objects.filter(faculty=faculty)
    
    context = {
        'faculty': faculty,
        'courses': courses
    }
    return render(request, 'faculty/faculty_detail.html', context)


@login_required
def edit_faculty(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    user = faculty.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
        
        user.save()

        faculty.department_id = request.POST.get('department')
        faculty.designation = request.POST.get('designation')
        faculty.joining_date = request.POST.get('joining_date')
        faculty.save()
        
        messages.success(request, 'Faculty updated successfully.')
        return redirect('faculty_list')
    
    departments = Department.objects.all()
    return render(request, 'faculty/edit_faculty.html', {'faculty': faculty, 'departments': departments})


@login_required
def delete_faculty(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        # Deleting the user will cascade delete the Faculty profile
        faculty.user.delete()
        messages.success(request, 'Faculty deleted successfully.')
        return redirect('faculty_list')
    return render(request, 'faculty/faculty_confirm_delete.html', {'faculty': faculty})


# ═══════════════════════════════════════════════════════════════════════════
#  1. TEACHER DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_dashboard(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty)
    total_courses = courses.count()

    # Total students across all courses
    total_students = 0
    for c in courses:
        total_students += c.students.count()

    # Pending grading = exams whose results are not yet complete
    pending_grading = 0
    exams = Exam.objects.filter(course__in=courses)
    for exam in exams:
        enrolled = exam.course.students.count()
        graded = Result.objects.filter(exam=exam).count()
        if graded < enrolled:
            pending_grading += 1

    # Notices posted by this teacher
    notices_count = Notice.objects.filter(posted_by=request.user).count()

    # Today's schedule from Timetable
    today = timezone.localdate()
    day_name = calendar.day_name[today.weekday()]
    todays_schedule = Timetable.objects.filter(
        faculty=faculty,
        day_of_week__iexact=day_name
    ).select_related('course').order_by('start_time')

    context = {
        'total_courses': total_courses,
        'total_students': total_students,
        'pending_grading': pending_grading,
        'notices_count': notices_count,
        'courses': courses,
        'todays_schedule': todays_schedule,
        'today_display': today.strftime('%A, %d %b %Y'),
    }
    return render(request, 'teacher/dashboard.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  2. MY COURSES
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_my_courses(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty).select_related('department')
    return render(request, 'teacher/my_courses.html', {'courses': courses})


@faculty_required
def teacher_course_students(request, course_id):
    faculty = request.user.faculty
    course = get_object_or_404(Course, id=course_id, faculty=faculty)
    students = course.students.select_related('user', 'department').all()
    return render(request, 'teacher/course_students.html', {'course': course, 'students': students})


@faculty_required
def teacher_timetable(request):
    faculty = request.user.faculty
    
    # Get all timetable entries for this faculty
    timetable_entries = Timetable.objects.filter(faculty=faculty).select_related('course').order_by('day_of_week', 'start_time')
    
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {day: [] for day in week_days}
    
    for entry in timetable_entries:
        day = entry.day_of_week.capitalize()
        if day in schedule:
            schedule[day].append(entry)
            
    return render(request, 'teacher/timetable.html', {'schedule': schedule, 'week_days': week_days})


# ═══════════════════════════════════════════════════════════════════════════
#  3. TAKE ATTENDANCE
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_take_attendance(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty)

    selected_course = None
    selected_date = timezone.localdate()
    students = []
    existing_present = set()
    already_marked = False

    # GET – load students
    if request.GET.get('course'):
        try:
            selected_course = Course.objects.get(id=request.GET['course'], faculty=faculty)
        except Course.DoesNotExist:
            selected_course = None

        if request.GET.get('date'):
            try:
                from datetime import datetime as dt
                selected_date = dt.strptime(request.GET['date'], '%Y-%m-%d').date()
            except ValueError:
                pass

        if selected_course:
            students = list(selected_course.students.select_related('user').all())
            # Check if attendance already exists for that date
            existing = Attendance.objects.filter(course=selected_course, date=selected_date).first()
            if existing:
                already_marked = True
                existing_present = set(
                    AttendanceRecord.objects.filter(attendance=existing, status=True)
                    .values_list('student_id', flat=True)
                )

    # POST – save attendance
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        date_str = request.POST.get('date')
        try:
            from datetime import datetime as dt
            att_date = dt.strptime(date_str, '%Y-%m-%d').date()
            course = Course.objects.get(id=course_id, faculty=faculty)
        except Exception:
            messages.error(request, 'Invalid course or date.')
            return redirect('teacher_take_attendance')

        # Create or get attendance session
        attendance_obj, created = Attendance.objects.get_or_create(
            course=course, date=att_date,
            defaults={'marked_by': faculty}
        )
        if not created:
            # Update: remove old records
            AttendanceRecord.objects.filter(attendance=attendance_obj).delete()

        enrolled_students = course.students.all()
        for student in enrolled_students:
            is_present = request.POST.get(f'present_{student.id}') == 'on'
            AttendanceRecord.objects.create(
                attendance=attendance_obj,
                student=student,
                status=is_present
            )

        messages.success(request, f'Attendance saved for {course.name} on {att_date.strftime("%d %b %Y")}.')
        return redirect('teacher_take_attendance')

    context = {
        'courses': courses,
        'selected_course': selected_course,
        'selected_date': selected_date,
        'students': students,
        'existing_present': existing_present,
        'already_marked': already_marked,
    }
    return render(request, 'teacher/take_attendance.html', context)


#  7. REPORTS


# ═══════════════════════════════════════════════════════════════════════════
#  4. UPLOAD MARKS
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_upload_marks(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty)
    exams = Exam.objects.filter(course__in=courses).select_related('course').order_by('-date')

    selected_exam = None
    student_marks = []

    if request.GET.get('exam'):
        try:
            selected_exam = Exam.objects.get(id=request.GET['exam'], course__faculty=faculty)
        except Exam.DoesNotExist:
            selected_exam = None

        if selected_exam:
            enrolled = selected_exam.course.students.select_related('user').all()
            for student in enrolled:
                result = Result.objects.filter(exam=selected_exam, student=student).first()
                student_marks.append({
                    'student': student,
                    'marks': result.marks_obtained if result else None,
                })

    context = {
        'exams': exams,
        'selected_exam': selected_exam,
        'student_marks': student_marks,
    }
    return render(request, 'teacher/upload_marks.html', context)


@faculty_required
def teacher_enter_marks(request, exam_id):
    faculty = request.user.faculty
    exam = get_object_or_404(Exam, id=exam_id, course__faculty=faculty)

    if exam.is_published:
        messages.error(request, 'Results for this exam are published and locked. You cannot modify them.')
        return redirect(f"{reverse('teacher_upload_marks')}?exam={exam.id}")

    if request.method == 'POST':
        enrolled = exam.course.students.all()
        for student in enrolled:
            marks_val = request.POST.get(f'marks_{student.id}')
            if marks_val is not None and marks_val.strip() != '':
                try:
                    marks = Decimal(marks_val)
                except Exception:
                    continue
                result, created = Result.objects.get_or_create(
                    exam=exam, student=student,
                    defaults={'marks_obtained': marks}
                )
                if not created:
                    result.marks_obtained = marks
                    result.save()

        messages.success(request, f'Marks saved for {exam.course.name} – {exam.get_exam_type_display()}.')
    return redirect(f"{reverse('teacher_upload_marks')}?exam={exam.id}")


# ═══════════════════════════════════════════════════════════════════════════
#  5. NOTICES
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_notices(request):
    notices = Notice.objects.filter(
        Q(posted_by=request.user) | 
        Q(target_audience='ALL') | 
        Q(target_audience='FACULTY')
    ).order_by('-created_at')
    return render(request, 'teacher/notices.html', {'notices': notices})


@faculty_required
def teacher_post_notice(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        target_audience = request.POST.get('target_audience', 'ALL')
        target_course_id = request.POST.get('target_course')
        attachment = request.FILES.get('attachment')

        notice = Notice(
            title=title,
            description=description,
            target_audience=target_audience,
            posted_by=request.user,
        )
        if target_course_id:
            try:
                notice.target_course = Course.objects.get(id=target_course_id, faculty=faculty)
            except Course.DoesNotExist:
                pass
        if attachment:
            notice.attachment = attachment
        notice.save()

        messages.success(request, 'Notice posted successfully.')
        return redirect('teacher_notices')

    return render(request, 'teacher/post_notice.html', {'courses': courses})


# ═══════════════════════════════════════════════════════════════════════════
#  6. VIEW STUDENTS
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_view_students(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty)

    selected_course_id = request.GET.get('course')
    if selected_course_id:
        try:
            selected_course_id = int(selected_course_id)
            course = Course.objects.get(id=selected_course_id, faculty=faculty)
            students = course.students.select_related('user', 'department').all()
        except (ValueError, Course.DoesNotExist):
            selected_course_id = None
            students = Student.objects.filter(
                enrolled_courses__faculty=faculty
            ).select_related('user', 'department').distinct()
    else:
        selected_course_id = None
        students = Student.objects.filter(
            enrolled_courses__faculty=faculty
        ).select_related('user', 'department').distinct()

    context = {
        'courses': courses,
        'students': students,
        'selected_course_id': selected_course_id,
    }
    return render(request, 'teacher/view_students.html', context)


@faculty_required
def teacher_student_profile(request, student_id):
    faculty = request.user.faculty
    student = get_object_or_404(Student, id=student_id)

    # Attendance for courses taught by this faculty
    faculty_courses = Course.objects.filter(faculty=faculty)
    attendance_records = AttendanceRecord.objects.filter(
        student=student,
        attendance__course__in=faculty_courses
    )
    total_classes = attendance_records.count()
    present_count = attendance_records.filter(status=True).count()
    attendance_pct = round(present_count / total_classes * 100, 1) if total_classes > 0 else 0

    # Results for courses taught by this faculty
    results = Result.objects.filter(
        student=student,
        exam__course__in=faculty_courses
    ).select_related('exam', 'exam__course').order_by('-exam__date')

    context = {
        'student': student,
        'total_classes': total_classes,
        'present_count': present_count,
        'attendance_pct': attendance_pct,
        'results': results,
    }
    return render(request, 'teacher/student_profile.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  7. REPORTS
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_reports(request):
    faculty = request.user.faculty
    courses = Course.objects.filter(faculty=faculty)

    selected_course = None
    report_type = request.GET.get('report_type', 'performance')
    report_data = []
    summary = {}
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if request.GET.get('course'):
        try:
            selected_course = Course.objects.get(id=request.GET['course'], faculty=faculty)
        except Course.DoesNotExist:
            pass

    if selected_course:
        enrolled = selected_course.students.select_related('user').all()

        if report_type == 'attendance':
            # Attendance report
            for student in enrolled:
                records = AttendanceRecord.objects.filter(
                    student=student,
                    attendance__course=selected_course
                )
                
                if start_date:
                    records = records.filter(attendance__date__gte=start_date)
                if end_date:
                    records = records.filter(attendance__date__lte=end_date)
                
                total = records.count()
                present = records.filter(status=True).count()
                absent = total - present
                pct = round(present / total * 100, 1) if total > 0 else 0
                report_data.append({
                    'enrollment_no': student.enrollment_no,
                    'name': student.user.get_full_name(),
                    'total': total,
                    'present': present,
                    'absent': absent,
                    'pct': pct,
                })
        else:
            # Performance report
            results = Result.objects.filter(
                exam__course=selected_course
            ).select_related('student', 'student__user', 'exam')

            all_marks = []
            passed_count = 0
            total_results = 0

            for r in results:
                is_passed = r.marks_obtained >= 40
                report_data.append({
                    'enrollment_no': r.student.enrollment_no,
                    'name': r.student.user.get_full_name(),
                    'exam_type': r.exam.get_exam_type_display(),
                    'exam_date': r.exam.date,
                    'marks': r.marks_obtained,
                    'total': r.exam.total_marks,
                    'passed': is_passed,
                })
                all_marks.append(float(r.marks_obtained))
                if is_passed:
                    passed_count += 1
                total_results += 1

            if all_marks:
                summary = {
                    'avg_marks': sum(all_marks) / len(all_marks),
                    'highest': max(all_marks),
                    'lowest': min(all_marks),
                    'pass_rate': (passed_count / total_results * 100) if total_results > 0 else 0,
                }

    context = {
        'courses': courses,
        'selected_course': selected_course,
        'report_type': report_type,
        'report_data': report_data,
        'summary': summary,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'teacher/reports.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  8. TEACHER PROFILE
# ═══════════════════════════════════════════════════════════════════════════
@faculty_required
def teacher_profile(request):
    faculty = request.user.faculty

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('teacher_profile')

    return render(request, 'teacher/profile.html', {'faculty': faculty})

