from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'ADMIN' or user.is_superuser:
        return redirect('admin_dashboard')
    elif user.role == 'FACULTY':
        return redirect('teacher_dashboard')
    elif user.role == 'STUDENT':
        return redirect('student_dashboard')
    elif user.role == 'ACCOUNTANT':
        return redirect('accountant_dashboard')
    else:
        return redirect('login') 
