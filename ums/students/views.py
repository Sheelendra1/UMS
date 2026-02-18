from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student
from departments.models import Department
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import random
import string

# Soft dependencies
from attendance.models import AttendanceRecord
from examinations.models import Result
from fees.models import FeeStructure, FeePayment

@login_required
def student_list(request):
    students = Student.objects.select_related('user', 'department').all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Attendance Stats
    attendance_records = AttendanceRecord.objects.filter(student=student)
    total_attendance = attendance_records.count()
    present_attendance = attendance_records.filter(status=True).count()
    attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    # Results
    results = Result.objects.filter(student=student).select_related('exam', 'exam__course')
    
    # Fees
    try:
        fee_structures = FeeStructure.objects.filter(department=student.department, semester=student.semester)
        total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = FeePayment.objects.filter(student=student, status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        pending_dues = total_payable - total_paid
    except:
        total_payable = 0
        total_paid = 0
        pending_dues = 0

    context = {
        'student': student,
        'attendance_percentage': round(attendance_percentage, 2),
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'results': results,
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
            user.set_password(password)
            user.save()

            dept = Department.objects.get(id=dept_id)
            Student.objects.create(
                user=user,
                enrollment_no=enrollment_no,
                department=dept,
                semester=semester,
                admission_date=admission_date
            )
            messages.success(request, f'Student created. Password: {password}')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Error adding student: {e}')
    
    departments = Department.objects.all()
    return render(request, 'students/add_student.html', {'departments': departments})

@login_required
def student_dashboard(request):
    try:
        student = request.user.student
        
        # Attendance
        attendance_records = AttendanceRecord.objects.filter(student=student)
        total_attendance = attendance_records.count()
        present_attendance = attendance_records.filter(status=True).count()
        attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
        
        # Fee Status
        fee_structures = FeeStructure.objects.filter(department=student.department, semester=student.semester)
        total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = FeePayment.objects.filter(student=student, status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        pending_dues = total_payable - total_paid
        
        # Recent Results
        recent_results = Result.objects.filter(student=student).select_related('exam', 'exam__course').order_by('-exam__date')[:5]

    except Exception:
        student = None
        attendance_percentage = 0
        pending_dues = 0
        recent_results = []
        total_attendance = 0
        present_attendance = 0
        total_payable = 0
        total_paid = 0

    context = {
        'student': student,
        'attendance_percentage': round(attendance_percentage, 2),
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'pending_dues': pending_dues,
        'total_paid': total_paid,
        'total_payable': total_payable,
        'recent_results': recent_results,
    }
    return render(request, 'student/dashboard.html', context)
