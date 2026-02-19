from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Exam, Result
from .forms import ExamForm
from students.models import Student
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'examinations/exam_list.html'
    context_object_name = 'exams'
    ordering = ['-date']

class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'examinations/exam_form.html'
    success_url = reverse_lazy('exam_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Exam scheduled successfully.")
        return super().form_valid(form)

class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'examinations/exam_form.html'
    success_url = reverse_lazy('exam_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Exam updated successfully.")
        return super().form_valid(form)

class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'examinations/exam_confirm_delete.html'
    success_url = reverse_lazy('exam_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Exam deleted successfully.")
        return super().delete(request, *args, **kwargs)

@login_required
def result_entry(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    
    if exam.is_published:
        messages.error(request, "Results are published and locked. You cannot modify them.")
        return redirect('exam_list')

    students = exam.course.students.all()
    
    if request.method == 'POST':
        try:
            for student in students:
                marks = request.POST.get(f'marks_{student.id}')
                if marks:
                    Result.objects.update_or_create(
                        exam=exam,
                        student=student,
                        defaults={'marks_obtained': marks}
                    )
            messages.success(request, "Results updated successfully.")
            return redirect('exam_list')
        except Exception as e:
            messages.error(request, f"Error updating results: {e}")

    # Fetch existing results
    results = Result.objects.filter(exam=exam)
    result_map = {res.student.id: res.marks_obtained for res in results}

    student_data = []
    for student in students:
        student_data.append({
            'student': student,
            'marks': result_map.get(student.id, '')
        })

    return render(request, 'examinations/result_entry.html', {
        'exam': exam,
        'student_data': student_data
    })

@login_required
def result_sheet(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    results = Result.objects.filter(exam=exam).select_related('student', 'student__user').order_by('student__enrollment_no')
    
    return render(request, 'examinations/result_sheet.html', {
        'exam': exam,
        'results': results
    })

@login_required
def publish_exam(request, pk):
    """
    Toggle the publication status of an exam result.
    If published, students can see their results.
    """
    exam = get_object_or_404(Exam, pk=pk)
    # Toggle status
    exam.is_published = not exam.is_published
    exam.save()
    
    status_msg = "published" if exam.is_published else "unpublished"
    messages.success(request, f"Exam results {status_msg} successfully.")
    
    return redirect('exam_list')
