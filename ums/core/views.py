from django.shortcuts import render, redirect
from django.db.models import Sum
from students.models import Student
from faculty.models import Faculty
from courses.models import Course
from fees.models import FeePayment
from django.contrib.admin.models import LogEntry
from django.contrib import messages
from .models import UniversitySetting

def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Faculty.objects.count()
    total_courses = Course.objects.count()
    # Calculate total revenue
    total_revenue_agg = FeePayment.objects.aggregate(Sum('amount_paid'))
    total_revenue = total_revenue_agg['amount_paid__sum'] or 0
    
    # Recent activities (from Django admin log)
    recent_activities = LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:5]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_revenue': total_revenue,
        'recent_activities': recent_activities,
    }
    return render(request, 'core/admin_dashboard.html', context)

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
