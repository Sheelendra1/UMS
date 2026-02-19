from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Notice

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'
    ordering = ['-created_at']

class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    fields = ['title', 'description', 'target_audience', 'attachment']
    template_name = 'notices/notice_form.html'
    success_url = reverse_lazy('notice_list')
    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, "Notice posted successfully.")
        return super().form_valid(form)

class NoticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Notice
    template_name = 'notices/notice_confirm_delete.html'
    success_url = reverse_lazy('notice_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Notice deleted successfully.")
        return super().form_valid(form)
