from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Course
from students.models import Student

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['name', 'code', 'department', 'faculty', 'semester', 'credits', 'capacity']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, "Course created successfully.")
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['name', 'code', 'department', 'faculty', 'semester', 'credits', 'capacity']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, "Course updated successfully.")
        return super().form_valid(form)

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Course deleted successfully.")
        return super().delete(request, *args, **kwargs)


@login_required
def enroll_students(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # Students must be in same Dept and Semester to be eligible
    eligible_students = Student.objects.filter(
        department=course.department,
        semester=course.semester
    ).exclude(enrolled_courses=course).select_related('user').order_by('enrollment_no')

    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        if student_ids:
            students_to_enroll = Student.objects.filter(id__in=student_ids)
            course.students.add(*students_to_enroll)
            messages.success(request, f"Successfully enrolled {students_to_enroll.count()} students in {course.code} - {course.name}.")
            return redirect('course_list')
        else:
            messages.warning(request, "No students selected.")

    return render(request, 'courses/enroll_students.html', {
        'course': course,
        'eligible_students': eligible_students
    })

