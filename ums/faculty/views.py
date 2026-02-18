from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Faculty
from departments.models import Department
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from courses.models import Course
import random
import string

@login_required
def faculty_list(request):
    faculty_members = Faculty.objects.select_related('user', 'department').all()
    return render(request, 'faculty/faculty_list.html', {'faculty_members': faculty_members})

@login_required
def add_faculty(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        dept_id = request.POST.get('department')
        designation = request.POST.get('designation')
        joining_date = request.POST.get('joining_date')
        password = request.POST.get('password')
        auto_gen = request.POST.get('auto_generate')

        if auto_gen or not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        try:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('add_faculty')

            user = CustomUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=CustomUser.Role.FACULTY
            )
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
def teacher_dashboard(request):
    try:
        faculty = request.user.faculty
        courses = Course.objects.filter(faculty=faculty)
        total_courses = courses.count()
        
        total_students_taught = 0
        for c in courses:
            total_students_taught += c.students.count()

    except Exception:
        courses = []
        total_courses = 0
        total_students_taught = 0

    context = {
        'total_courses': total_courses,
        'total_students_taught': total_students_taught,
        'courses': courses
    }
    return render(request, 'teacher/dashboard.html', context)
