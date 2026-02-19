from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from core.utils import render_to_pdf, log_activity
from django.contrib.admin.models import ADDITION
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from decimal import Decimal

from .models import Student
from departments.models import Department
from accounts.models import CustomUser
from courses.models import Course
from attendance.models import Attendance, AttendanceRecord
from examinations.models import Exam, Result
from fees.models import FeeStructure, FeePayment
from notices.models import Notice
from timetable.models import Timetable
from django.contrib.auth.hashers import make_password
import random
import string


# ── Helper ───────────────────────────────────────────────────────────────────
def student_required(view_func):
    """Decorator: user must be logged-in AND be a Student."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student'):
            messages.error(request, 'Access denied. Student account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


# ── Admin-facing views (unchanged) ──────────────────────────────────────────
@login_required
def student_list(request):
    dept_id = request.GET.get('department')
    semester = request.GET.get('semester')
    search_query = request.GET.get('q')

    students = Student.objects.select_related('user', 'department').all()

    if dept_id:
        students = students.filter(department_id=dept_id)
    if semester:
        students = students.filter(semester=semester)
    if search_query:
        students = students.filter(
            Q(enrollment_no__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    departments = Department.objects.all()
    
    return render(request, 'students/student_list.html', {
        'students': students,
        'departments': departments,
        'selected_dept': int(dept_id) if dept_id and dept_id.isdigit() else None,
        'selected_sem': int(semester) if semester and semester.isdigit() else None,
        'search_query': search_query
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    attendance_records = AttendanceRecord.objects.filter(student=student)
    total_attendance = attendance_records.count()
    present_attendance = attendance_records.filter(status=True).count()
    attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0

    results = Result.objects.filter(student=student).select_related('exam', 'exam__course')
    
    # Fees
    payments = FeePayment.objects.filter(student=student).order_by('-payment_date')

    try:
        fee_structures = FeeStructure.objects.filter(department=student.department, semester=student.semester)
        total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = payments.filter(status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        pending_dues = total_payable - total_paid
    except Exception:
        total_payable = total_paid = pending_dues = 0

    context = {
        'student': student,
        'attendance_percentage': round(attendance_percentage, 2),
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'attendance_records': attendance_records.select_related('attendance', 'attendance__course').order_by('-attendance__date')[:50], # Recent 50
        'results': results,
        'payments': payments,
        'total_payable': total_payable,
        'total_paid': total_paid,
        'pending_dues': pending_dues,
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        enrollment_no = request.POST.get('enrollment_no')
        dept_id = request.POST.get('department')
        semester = request.POST.get('semester')
        admission_date = request.POST.get('admission_date')
        password = request.POST.get('password')
        auto_gen = request.POST.get('auto_generate')

        if auto_gen or not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        try:
            if CustomUser.objects.filter(username=enrollment_no).exists():
                messages.error(request, 'Username/Enrollment already exists.')
                return redirect('add_student')

            user = CustomUser.objects.create(
                username=enrollment_no,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=CustomUser.Role.STUDENT
            )
            if request.FILES.get('profile_image'):
                user.profile_image = request.FILES['profile_image']
            user.set_password(password)
            user.save()

            dept = Department.objects.get(id=dept_id)
            student_obj = Student.objects.create(
                user=user,
                enrollment_no=enrollment_no,
                department=dept,
                semester=semester,
                admission_date=admission_date
            )
            log_activity(request.user, student_obj, ADDITION, "Student Added")
            messages.success(request, f'Student created. Password: {password}')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Error adding student: {e}')

    departments = Department.objects.all()
    return render(request, 'students/add_student.html', {'departments': departments})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = student.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
        
        user.save()

        student.department_id = request.POST.get('department')
        student.semester = request.POST.get('semester')
        student.admission_date = request.POST.get('admission_date')
        student.save()
        
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')
    
    departments = Department.objects.all()
    return render(request, 'students/edit_student.html', {'student': student, 'departments': departments})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        # Deleting the user will cascade delete the Student profile
        student.user.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
def promote_students(request):
    """
    View for promoting students to the next semester.
    Allows filtering by Department and Current Semester.
    Then selecting students to promote.
    """
    departments = Department.objects.all()
    selected_dept = request.GET.get('department')
    selected_sem = request.GET.get('semester')
    students = []

    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        if student_ids:
            try:
                # We need to know the current semester to increment it.
                # Assuming all selected students are from the filtered view (so same semester).
                # But safer to iterate or update. 
                # Since bulk update to `semester + 1` is cleaner if we use F expression, 
                # but we need to import F.
                # Or just fetch and update.
                
                # Let's use the selected_sem from form or query param if available.
                # But users might inspect element.
                # Safer: Fetch students and increment their semester individually or bulk update with F.
                
                from django.db.models import F
                count = Student.objects.filter(id__in=student_ids).update(semester=F('semester') + 1)
                
                messages.success(request, f"Successfully promoted {count} students.")
                
                # Redirect to the NEW semester view? Or stay on the old one (which will now be empty)?
                # Staying on old one (empty) confirms they moved.
                # Redirecting to new one shows them in new state.
                # Let's stay on current filter so user sees they are gone.
                return redirect(f"{reverse('promote_students')}?department={selected_dept}&semester={selected_sem}")
            except Exception as e:
                messages.error(request, f"Error promoting students: {e}")
        else:
            messages.warning(request, "No students selected for promotion.")

    if selected_dept and selected_sem:
        try:
            students = Student.objects.filter(
                department_id=selected_dept, 
                semester=selected_sem
            ).select_related('user').order_by('enrollment_no')
        except ValueError:
            pass # Handle non-integer semester

    context = {
        'departments': departments,
        'selected_dept': int(selected_dept) if selected_dept and selected_dept.isdigit() else None,
        'selected_sem': int(selected_sem) if selected_sem and selected_sem.isdigit() else None,
        'students': students,
    }
    return render(request, 'students/promote_students.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  1. STUDENT DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_dashboard(request):
    student = request.user.student
    courses = Course.objects.filter(students=student).select_related('department', 'faculty', 'faculty__user')
    enrolled_count = courses.count()

    # Attendance
    att_records = AttendanceRecord.objects.filter(student=student)
    total_att = att_records.count()
    present_att = att_records.filter(status=True).count()
    attendance_percentage = round(present_att / total_att * 100, 1) if total_att > 0 else 0

    # Fee Status
    try:
        fee_structures = FeeStructure.objects.filter(department=student.department, semester=student.semester)
        total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = FeePayment.objects.filter(student=student, status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        pending_dues = total_payable - total_paid
    except Exception:
        total_payable = total_paid = 0
        pending_dues = 0

    # Upcoming exams
    today = timezone.localdate()
    upcoming_exams = Exam.objects.filter(
        course__in=courses,
        date__gte=today
    ).select_related('course').order_by('date')[:5]
    upcoming_exams_count = Exam.objects.filter(course__in=courses, date__gte=today).count()

    # Recent results
    recent_results = Result.objects.filter(
        student=student
    ).select_related('exam', 'exam__course').order_by('-exam__date')[:5]

    context = {
        'student': student,
        'courses': courses[:6],
        'enrolled_count': enrolled_count,
        'attendance_percentage': attendance_percentage,
        'pending_dues': pending_dues,
        'upcoming_exams': upcoming_exams,
        'upcoming_exams_count': upcoming_exams_count,
        'recent_results': recent_results,
    }
    return render(request, 'student/dashboard.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  2. MY COURSES
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_my_courses(request):
    student = request.user.student
    courses = Course.objects.filter(students=student).select_related(
        'department', 'faculty', 'faculty__user'
    )
    return render(request, 'student/my_courses.html', {'courses': courses})


@student_required
def student_course_detail(request, course_id):
    student = request.user.student
    course = get_object_or_404(Course, id=course_id, students=student)

    # Attendance for this course
    att_records = AttendanceRecord.objects.filter(
        student=student, attendance__course=course
    )
    total = att_records.count()
    present = att_records.filter(status=True).count()
    absent = total - present
    pct = round(present / total * 100, 1) if total > 0 else 0
    attendance = {'total': total, 'present': present, 'absent': absent, 'pct': pct}

    # Results for this course
    results = Result.objects.filter(
        student=student, exam__course=course
    ).select_related('exam').order_by('-exam__date')

    # Schedule
    schedule = Timetable.objects.filter(course=course).order_by('day_of_week', 'start_time')

    context = {
        'course': course,
        'attendance': attendance,
        'results': results,
        'schedule': schedule,
    }
    return render(request, 'student/course_detail.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  3. MY ATTENDANCE
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_my_attendance(request):
    student = request.user.student
    courses = Course.objects.filter(students=student)

    # Filters
    selected_course_id = request.GET.get('course')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    records_qs = AttendanceRecord.objects.filter(
        student=student
    ).select_related('attendance', 'attendance__course').order_by('-attendance__date')

    if selected_course_id:
        try:
            selected_course_id = int(selected_course_id)
            records_qs = records_qs.filter(attendance__course_id=selected_course_id)
        except ValueError:
            selected_course_id = None

    if start_date:
        records_qs = records_qs.filter(attendance__date__gte=start_date)
    if end_date:
        records_qs = records_qs.filter(attendance__date__lte=end_date)

    records = list(records_qs)

    # Course-wise attendance summary
    course_summary = []
    for course in courses:
        c_records = AttendanceRecord.objects.filter(student=student, attendance__course=course)
        total = c_records.count()
        present = c_records.filter(status=True).count()
        absent = total - present
        pct = round(present / total * 100, 1) if total > 0 else 0
        course_summary.append({
            'course_name': course.name,
            'course_code': course.code,
            'total': total,
            'present': present,
            'absent': absent,
            'pct': pct,
        })

    context = {
        'courses': courses,
        'records': records,
        'course_summary': course_summary,
        'selected_course_id': selected_course_id,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'student/my_attendance.html', context)


from core.utils import render_to_pdf

# ═══════════════════════════════════════════════════════════════════════════
#  4. MY RESULTS
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_my_results(request):
    student = request.user.student
    courses = Course.objects.filter(students=student)

    results_qs = Result.objects.filter(
        student=student
    ).select_related('exam', 'exam__course').order_by('-exam__date')

    # Filters
    selected_course_id = request.GET.get('course')
    selected_exam_type = request.GET.get('exam_type')

    if selected_course_id:
        try:
            selected_course_id = int(selected_course_id)
            results_qs = results_qs.filter(exam__course_id=selected_course_id)
        except ValueError:
            selected_course_id = None

    if selected_exam_type:
        results_qs = results_qs.filter(exam__exam_type=selected_exam_type)

    results = list(results_qs)

    # Summary
    summary = {}
    if results:
        marks_list = [float(r.marks_obtained) for r in results]
        total_marks = [float(r.exam.total_marks) for r in results]
        pct_list = [(m / t * 100) if t > 0 else 0 for m, t in zip(marks_list, total_marks)]
        passed = sum(1 for m in marks_list if m >= 40)
        summary = {
            'total_exams': len(results),
            'avg_pct': sum(pct_list) / len(pct_list) if pct_list else 0,
            'highest': max(marks_list),
            'passed': passed,
        }

    context = {
        'courses': courses,
        'results': results,
        'summary': summary,
        'selected_course_id': selected_course_id,
        'selected_exam_type': selected_exam_type or '',
    }
    return render(request, 'student/my_results.html', context)


@student_required
def download_results_pdf(request):
    """
    Generate PDF of student transcript.
    """
    student = request.user.student
    
    # Fetch all results ordered by date
    results = Result.objects.filter(student=student).select_related(
        'exam', 'exam__course', 'exam__course__department'
    ).order_by('exam__date')
    
    # Calculate Summary
    total_marks_obtained = 0
    total_max_marks = 0
    passed_count = 0
    
    for r in results:
        total_marks_obtained += r.marks_obtained
        total_max_marks += r.exam.total_marks
        if (r.marks_obtained / r.exam.total_marks) * 100 >= 40: # Assuming 40% pass
            passed_count += 1
            
    percentage = (total_marks_obtained / total_max_marks * 100) if total_max_marks > 0 else 0
    
    context = {
        'student': student,
        'results': results,
        'total_obtained': total_marks_obtained,
        'total_max': total_max_marks,
        'percentage': round(percentage, 2),
        'generated_at': timezone.now(),
    }
    
    pdf = render_to_pdf('student/my_results_pdf.html', context)
    if pdf:
        filename = f"Transcript_{student.enrollment_no}.pdf"
        content = f"inline; filename={filename}"
        pdf['Content-Disposition'] = content
        return pdf
    return HttpResponse("Error Generating PDF", status=500)


@student_required
def download_id_card_pdf(request):
    """
    Generate Student ID Card PDF.
    """
    student = request.user.student
    # Basic logic: ID valid for 4 years from admission
    try:
        expire_year = student.admission_date.year + 4
        expire_date = student.admission_date.replace(year=expire_year)
    except ValueError: # Leap year edge case
        expire_date = student.admission_date.replace(year=expire_year, day=28)

    context = {
        'student': student,
        'expire_date': expire_date,
        'generated_at': timezone.now(),
        # Pass full URL for image if needed by xhtml2pdf, usually relies on STATIC_ROOT / MEDIA_ROOT handling in utils
    }
    
    pdf = render_to_pdf('student/id_card_pdf.html', context)
    if pdf:
        filename = f"ID_Card_{student.enrollment_no}.pdf"
        content = f"inline; filename={filename}"
        pdf['Content-Disposition'] = content
        return pdf
    return HttpResponse("Error Generating ID Card PDF", status=500)


@student_required
def download_receipt_pdf(request, payment_id):
    """
    Generate Fee Receipt PDF for Student.
    """
    student = request.user.student
    # Ensure the payment belongs to the logged-in student
    payment = get_object_or_404(FeePayment, id=payment_id, student=student)

    context = {
        'payment': payment,
        'student': student,
        'generated_at': timezone.now(),
    }
    
    pdf = render_to_pdf('student/receipt_pdf.html', context)
    if pdf:
        filename = f"Receipt_{payment.receipt_no}.pdf"
        content = f"inline; filename={filename}"
        pdf['Content-Disposition'] = content
        return pdf
    return HttpResponse("Error Generating Receipt PDF", status=500)



# ═══════════════════════════════════════════════════════════════════════════
#  5. FEE STATUS
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_fee_status(request):
    student = request.user.student

    fee_structures = FeeStructure.objects.filter(
        department=student.department, semester=student.semester
    ).select_related('department')
    total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0

    payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
    total_paid = payments.filter(status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    pending_dues = total_payable - total_paid

    context = {
        'fee_structures': fee_structures,
        'payments': payments,
        'total_payable': total_payable,
        'total_paid': total_paid,
        'pending_dues': pending_dues,
    }
    return render(request, 'student/fee_status.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  6. NOTICES
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_notices(request):
    student = request.user.student
    enrolled_courses = Course.objects.filter(students=student)

    filter_type = request.GET.get('type', 'all')

    # Notices targeted at ALL or STUDENT, plus course-specific notices for
    # courses this student is enrolled in
    notices_qs = Notice.objects.filter(
        Q(target_audience__in=['ALL', 'STUDENT']) |
        Q(target_course__in=enrolled_courses)
    ).distinct().order_by('-created_at')

    if filter_type == 'general':
        notices_qs = notices_qs.filter(target_course__isnull=True)
    elif filter_type == 'course':
        notices_qs = notices_qs.filter(target_course__isnull=False)

    context = {
        'notices': notices_qs,
        'filter_type': filter_type,
    }
    return render(request, 'student/notices.html', context)


@student_required
def student_timetable(request):
    student = request.user.student
    courses = Course.objects.filter(students=student)
    
    # Get all timetable entries for enrolled courses
    timetable_entries = Timetable.objects.filter(course__in=courses).select_related('course', 'faculty', 'faculty__user').order_by('day_of_week', 'start_time')
    
    # Organize by day
    # Assuming day_of_week is a string like "Monday"
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {day: [] for day in week_days}
    
    for entry in timetable_entries:
        # entry.day_of_week might be case-insensitive in DB, let's normalize capitalizaion if needed
        day = entry.day_of_week.capitalize()
        if day in schedule:
            schedule[day].append(entry)
            
    return render(request, 'student/timetable.html', {'schedule': schedule, 'week_days': week_days})


# ═══════════════════════════════════════════════════════════════════════════
#  7. STUDENT PROFILE
# ═══════════════════════════════════════════════════════════════════════════
@student_required
def student_profile(request):
    student = request.user.student

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', '')
        if hasattr(user, 'phone'):
            user.phone = phone

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('student_profile')

    return render(request, 'student/profile.html', {'student': student})
