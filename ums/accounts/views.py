from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .models import CustomUser

class UMBaseTemplateMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.role == CustomUser.Role.STUDENT:
                context['base_template'] = 'student/base_student.html'
            elif user.role == CustomUser.Role.FACULTY:
                context['base_template'] = 'teacher/base_teacher.html'
            elif user.role == CustomUser.Role.ACCOUNTANT:
                context['base_template'] = 'accountant/base_accountant.html'
            else:
                context['base_template'] = 'base.html'
        else:
            context['base_template'] = 'base.html'
        return context

class MainPasswordChangeView(UMBaseTemplateMixin, auth_views.PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    
class MainPasswordChangeDoneView(UMBaseTemplateMixin, auth_views.PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Implementation of "Remember Me" checkbox
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            # If not checked, session expires when browser closes (0 seconds)
            self.request.session.set_expiry(0)
        # If checked, uses Django's default session cookie age (usually 2 weeks)
        return super().form_valid(form)

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

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
