from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Sum
from .models import FeeStructure, FeePayment

class FeeStructureListView(LoginRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'fees/fee_structure_list.html'
    context_object_name = 'structures'
    ordering = ['department', 'semester']

class FeeStructureCreateView(LoginRequiredMixin, CreateView):
    model = FeeStructure
    fields = ['department', 'semester', 'amount']
    template_name = 'fees/fee_structure_form.html'
    success_url = reverse_lazy('fee_structure_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Fee structure created successfully.")
        return super().form_valid(form)

class FeePaymentListView(LoginRequiredMixin, ListView):
    model = FeePayment
    template_name = 'fees/payment_list.html'
    context_object_name = 'payments'
    ordering = ['-payment_date']

class FeePaymentCreateView(LoginRequiredMixin, CreateView):
    model = FeePayment
    fields = ['student', 'amount_paid', 'status']
    template_name = 'fees/payment_form.html'
    success_url = reverse_lazy('fee_payment_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Payment recorded successfully.")
        return super().form_valid(form)

@login_required
def accountant_dashboard(request):
    total_collections = FeePayment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    recent_payments = FeePayment.objects.select_related('student', 'student__user').order_by('-payment_date')[:10]
    
    context = {
        'total_collections': total_collections,
        'recent_payments': recent_payments,
    }
    return render(request, 'accountant/dashboard.html', context)
