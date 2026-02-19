from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q  # Added Q
from django.contrib import messages
from django.utils import timezone

from students.models import Student
from faculty.models import Faculty
from courses.models import Course
from departments.models import Department
from fees.models import FeePayment
from accounts.models import CustomUser
from django.contrib.admin.models import LogEntry
from notices.models import Notice
from .models import UniversitySetting


# ── Helper ───────────────────────────────────────────────────────────────────
def admin_required(view_func):
    """Decorator: user must be logged-in AND have ADMIN role or be superuser."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN' and not request.user.is_superuser:
            messages.error(request, 'Access denied. Admin account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


from attendance.models import AttendanceRecord

# ── Admin Dashboard ─────────────────────────────────────────────────────────
@admin_required
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Faculty.objects.count()
    total_courses = Course.objects.count()
    total_revenue_agg = FeePayment.objects.aggregate(Sum('amount_paid'))
    total_revenue = total_revenue_agg['amount_paid__sum'] or 0

    # Calculate Attendance Percentage
    total_records = AttendanceRecord.objects.count()
    presented_records = AttendanceRecord.objects.filter(status=True).count()
    attendance_percentage = (presented_records / total_records * 100) if total_records > 0 else 0

    recent_activities = LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:5]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_revenue': total_revenue,
        'attendance_percentage': round(attendance_percentage, 1),
        'recent_activities': recent_activities,
    }
    return render(request, 'core/admin_dashboard.html', context)


# ── Settings ────────────────────────────────────────────────────────────────
@admin_required
def settings_view(request):
    settings_obj = UniversitySetting.objects.first()
    if not settings_obj:
        settings_obj = UniversitySetting.objects.create()

    if request.method == 'POST':
        university_name = request.POST.get('university_name')
        if university_name:
            settings_obj.university_name = university_name

        academic_year = request.POST.get('academic_year')
        if academic_year:
            settings_obj.academic_year = academic_year

        current_semester = request.POST.get('current_semester')
        if current_semester:
            settings_obj.current_semester = current_semester

        if 'logo' in request.FILES:
            settings_obj.logo = request.FILES['logo']

        settings_obj.save()
        messages.success(request, "Settings updated successfully.")
        return redirect('settings')

    return render(request, 'core/settings.html', {'settings': settings_obj})


# ═══════════════════════════════════════════════════════════════════════════
#  COMMON / PUBLIC PAGES
# ═══════════════════════════════════════════════════════════════════════════

def _get_university_context():
    """Shared context for public-facing pages."""
    settings_obj = UniversitySetting.objects.first()
    return {
        'settings_obj': settings_obj,
        'university_name': settings_obj.university_name if settings_obj else 'My University',
        'academic_year': settings_obj.academic_year if settings_obj else '2024-2025',
        'current_semester': settings_obj.current_semester if settings_obj else 1,
        'current_year': timezone.localdate().year,
    }


# ── About University ────────────────────────────────────────────────────────
def about_university(request):
    ctx = _get_university_context()
    ctx.update({
        'total_students': Student.objects.count(),
        'total_faculty': Faculty.objects.count(),
        'total_courses': Course.objects.count(),
        'total_departments': Department.objects.count(),
        'departments': Department.objects.select_related('hod', 'hod__user').all(),
    })
    return render(request, 'common/about.html', ctx)


# ── Contact Page ────────────────────────────────────────────────────────────
def contact_page(request):
    ctx = _get_university_context()

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message_text = request.POST.get('message', '')

        # In production, send an email or save to a ContactMessage model.
        # For now, show a success message.
        messages.success(
            request,
            f'Thank you, {name}! Your message regarding "{subject}" has been received. '
            f'We\'ll get back to you at {email} shortly.'
        )
        return redirect('contact_page')

    return render(request, 'common/contact.html', ctx)


# ── Public Profile ──────────────────────────────────────────────────────────
def public_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    student = None
    faculty = None
    enrolled_courses = None
    teaching_courses = None

    if hasattr(profile_user, 'student'):
        student = profile_user.student
        enrolled_courses = Course.objects.filter(students=student).select_related('department')

    if hasattr(profile_user, 'faculty'):
        faculty = profile_user.faculty
        teaching_courses = Course.objects.filter(faculty=faculty).select_related('department')

    context = {
        'profile_user': profile_user,
        'student': student,
        'faculty': faculty,
        'enrolled_courses': enrolled_courses,
        'teaching_courses': teaching_courses,
    }
    return render(request, 'common/public_profile.html', context)


@login_required
def global_search(request):
    """
    Search across Students, Faculty, and Courses based on the query parameter 'q'.
    Each user role sees limited data if handled via custom permissions, 
    but for now we simply filter public info.
    """
    query = request.GET.get('q')
    results = {
        'students': [],
        'faculty': [],
        'courses': [],
    }
    
    if query:
        # Search Students (Name, Enrollment No)
        from students.models import Student
        from faculty.models import Faculty
        from courses.models import Course
        from django.db.models import Q

        results['students'] = Student.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(user__username__icontains=query) |
            Q(enrollment_no__icontains=query)
        ).select_related('user', 'department')[:10]

        # Search Faculty (Name, Department)
        results['faculty'] = Faculty.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
        ).select_related('user', 'department')[:10]

        # Search Courses (Name, Code)
        results['courses'] = Course.objects.filter(
            Q(name__icontains=query) | 
            Q(code__icontains=query)
        ).select_related('department')[:10]

    # Determine base template
    base_template = 'base.html'
    if request.user.is_authenticated:
        # Check role safely (assuming role attribute exists on user model)
        role = getattr(request.user, 'role', 'ADMIN') 
        if role == 'STUDENT':
            base_template = 'student/base_student.html'
        elif role == 'FACULTY':
            base_template = 'teacher/base_teacher.html'

    return render(request, 'core/search_results.html', {
        'query': query, 
        'results': results,
        'base_template': base_template
    })


# ── Custom Error Handlers ───────────────────────────────────────────────────
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_403(request, exception):
    return render(request, '403.html', status=403)
