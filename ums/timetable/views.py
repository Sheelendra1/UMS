from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Timetable
from courses.models import Course
from departments.models import Department
from faculty.models import Faculty
from .forms import TimetableForm

class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = 'timetable/timetable_list.html'
    context_object_name = 'timetables'
    ordering = ['day_of_week', 'start_time']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('course', 'faculty', 'course__department')
        
        department_id = self.request.GET.get('department')
        semester = self.request.GET.get('semester')
        course_id = self.request.GET.get('course')

        if department_id:
            queryset = queryset.filter(course__department_id=department_id)
        if semester:
            queryset = queryset.filter(course__semester=semester)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        # Assume 8 semesters for now, or fetch distinct values if preferred
        context['semesters'] = range(1, 9) 
        context['courses'] = Course.objects.all().order_by('name')
        
        # Pass current filter values to keep state in form
        context['selected_department'] = int(self.request.GET.get('department')) if self.request.GET.get('department') else None
        context['selected_semester'] = int(self.request.GET.get('semester')) if self.request.GET.get('semester') else None
        context['selected_course'] = int(self.request.GET.get('course')) if self.request.GET.get('course') else None
        
        return context

class TimetableCreateView(LoginRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'timetable/timetable_form.html'
    success_url = reverse_lazy('timetable_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Timetable entry created successfully.")
        return super().form_valid(form)

class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'timetable/timetable_form.html'
    success_url = reverse_lazy('timetable_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Timetable entry updated successfully.")
        return super().form_valid(form)
    
    def form_valid(self, form):
        messages.success(self.request, "Timetable entry updated successfully.")
        return super().form_valid(form)

class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    model = Timetable
    template_name = 'timetable/timetable_confirm_delete.html'
    success_url = reverse_lazy('timetable_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Timetable entry deleted successfully.")
        return super().delete(request, *args, **kwargs)
