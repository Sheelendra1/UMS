from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q, Count
from decimal import Decimal
from django.http import HttpResponse
from core.utils import render_to_pdf
import calendar

from .models import FeeStructure, FeePayment
from students.models import Student
from notices.models import Notice


# ── Helper ───────────────────────────────────────────────────────────────────
def accountant_required(view_func):
    """Decorator: user must be logged-in AND have ACCOUNTANT or ADMIN role."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ('ACCOUNTANT', 'ADMIN') and not request.user.is_superuser:
            messages.error(request, 'Access denied. Accountant account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


# ── Admin-facing CBVs (kept for backward compat) ───────────────────────────
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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


class FeeStructureUpdateView(LoginRequiredMixin, UpdateView):
    model = FeeStructure
    fields = ['department', 'semester', 'amount']
    template_name = 'fees/fee_structure_form.html'
    success_url = reverse_lazy('fee_structure_list')

    def form_valid(self, form):
        messages.success(self.request, "Fee structure updated successfully.")
        return super().form_valid(form)


class FeeStructureDeleteView(LoginRequiredMixin, DeleteView):
    model = FeeStructure
    template_name = 'fees/fee_structure_confirm_delete.html'
    success_url = reverse_lazy('fee_structure_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fee structure deleted successfully.")
        return super().delete(request, *args, **kwargs)



class FeePaymentListView(LoginRequiredMixin, ListView):
    model = FeePayment
    template_name = 'fees/payment_list.html'
    context_object_name = 'payments'
    ordering = ['-payment_date']

    def get_queryset(self):
        qs = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            qs = qs.filter(payment_date__gte=start_date)
        if end_date:
            qs = qs.filter(payment_date__lte=end_date)
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context


class FeePaymentCreateView(LoginRequiredMixin, CreateView):
    model = FeePayment
    fields = ['student', 'amount_paid', 'status', 'payment_mode']
    template_name = 'fees/payment_form.html'
    success_url = reverse_lazy('fee_payment_list')

    def form_valid(self, form):
        messages.success(self.request, "Payment recorded successfully.")
        return super().form_valid(form)


# ═══════════════════════════════════════════════════════════════════════════
#  1. ACCOUNTANT DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
@accountant_required
def accountant_dashboard(request):
    today = timezone.localdate()

    total_collected = FeePayment.objects.filter(status='PAID').aggregate(
        Sum('amount_paid'))['amount_paid__sum'] or 0

    total_pending = FeePayment.objects.filter(status='PENDING').aggregate(
        Sum('amount_paid'))['amount_paid__sum'] or 0

    this_month_collected = FeePayment.objects.filter(
        status='PAID',
        payment_date__year=today.year,
        payment_date__month=today.month
    ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    total_students = Student.objects.count()

    # Monthly revenue data (CSS bar chart)
    current_year = today.year
    monthly_data = []
    max_amount = 1  # avoid div by zero
    for m in range(1, 13):
        amt = FeePayment.objects.filter(
            status='PAID',
            payment_date__year=current_year,
            payment_date__month=m
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        monthly_data.append({
            'label': calendar.month_abbr[m],
            'amount': amt,
        })
        if amt > max_amount:
            max_amount = amt

    for item in monthly_data:
        item['height'] = round(float(item['amount']) / float(max_amount) * 100) if max_amount > 0 else 0

    recent_payments = FeePayment.objects.select_related(
        'student', 'student__user'
    ).order_by('-payment_date')[:10]

    context = {
        'total_collected': total_collected,
        'total_pending': total_pending,
        'this_month_collected': this_month_collected,
        'total_students': total_students,
        'monthly_data': monthly_data,
        'current_year': current_year,
        'recent_payments': recent_payments,
    }
    return render(request, 'accountant/dashboard.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  2. COLLECT FEES
# ═══════════════════════════════════════════════════════════════════════════
@accountant_required
def accountant_collect_fees(request):
    query = request.GET.get('q', '').strip()
    student_id = request.GET.get('student_id')
    search_results = None
    selected_student = None
    fee_info = {}

    # Search
    if query:
        search_results = Student.objects.filter(
            Q(enrollment_no__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
        ).select_related('user', 'department')[:10]

    # Select student
    if student_id:
        try:
            selected_student = Student.objects.select_related('user', 'department').get(id=student_id)
            fee_structures = FeeStructure.objects.filter(
                department=selected_student.department,
                semester=selected_student.semester
            )
            total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
            total_paid = FeePayment.objects.filter(
                student=selected_student, status='PAID'
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
            fee_info = {
                'total_payable': total_payable,
                'total_paid': total_paid,
                'pending': total_payable - total_paid,
            }
        except Student.DoesNotExist:
            selected_student = None

    # POST: record payment
    if request.method == 'POST':
        sid = request.POST.get('student_id')
        amount_str = request.POST.get('amount')
        payment_mode = request.POST.get('payment_mode', 'CASH')

        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                messages.error(request, "Amount must be greater than zero.")
            else:
                student = Student.objects.get(id=sid)
                
                # Validation: Check for overpayment
                # Calculate current pending dues
                fee_structures = FeeStructure.objects.filter(
                    department=student.department,
                    semester=student.semester
                )
                total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
                total_paid_so_far = FeePayment.objects.filter(
                    student=student, status='PAID'
                ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
                
                pending_dues = total_payable - total_paid_so_far
                
                if amount > pending_dues:
                    messages.error(request, f"Overpayment detected. Maximum pending due is ₹{pending_dues}. You entered ₹{amount}.")
                else:
                    payment = FeePayment.objects.create(
                        student=student,
                        amount_paid=amount,
                        status='PAID',  # Assuming immediate payment
                        payment_mode=payment_mode,
                        collected_by=request.user,
                    )
                    messages.success(
                        request,
                        f'Payment of ₹{amount} collected! Receipt: {payment.receipt_no}'
                    )
                    return redirect('accountant_receipt', payment_id=payment.id)

        except Exception as e:
            messages.error(request, f'Error recording payment: {e}')
        
        # If we failed (and didn't redirect), ensure we still have student context if possible
        # Since 'sid' is known, we can re-populate the context for the same student
        if sid:
            try:
                selected_student = Student.objects.select_related('user', 'department').get(id=sid)
                # Recalculate context for the view
                fee_structures = FeeStructure.objects.filter(
                    department=selected_student.department,
                    semester=selected_student.semester
                )
                total_payable = fee_structures.aggregate(Sum('amount'))['amount__sum'] or 0
                total_paid = FeePayment.objects.filter(
                    student=selected_student, status='PAID'
                ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
                fee_info = {
                    'total_payable': total_payable,
                    'total_paid': total_paid,
                    'pending': total_payable - total_paid,
                }
            except Student.DoesNotExist:
                pass

    context = {
        'query': query,
        'search_results': search_results,
        'selected_student': selected_student,
        'fee_info': fee_info,
    }
    return render(request, 'accountant/collect_fees.html', context)


# ═══════════════════════════════════════════════════════════════════════════
#  3. PAYMENT HISTORY
# ═══════════════════════════════════════════════════════════════════════════
@accountant_required
def accountant_payment_history(request):
    payments_qs = FeePayment.objects.select_related(
        'student', 'student__user'
    ).order_by('-payment_date')

    query = request.GET.get('q', '').strip()
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    if query:
        payments_qs = payments_qs.filter(
            Q(student__enrollment_no__icontains=query) |
            Q(student__user__first_name__icontains=query) |
            Q(student__user__last_name__icontains=query)
        )

    if from_date:
        payments_qs = payments_qs.filter(payment_date__gte=from_date)
    if to_date:
        payments_qs = payments_qs.filter(payment_date__lte=to_date)

    context = {
        'payments': payments_qs[:100],
        'query': query,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'accountant/payment_history.html', context)


@accountant_required
def accountant_receipt(request, payment_id):
    payment = get_object_or_404(
        FeePayment.objects.select_related('student', 'student__user', 'student__department', 'collected_by'),
        id=payment_id
    )
    return render(request, 'accountant/receipt.html', {'payment': payment})


# ═══════════════════════════════════════════════════════════════════════════
#  4. FINANCIAL REPORTS
# ═══════════════════════════════════════════════════════════════════════════
@accountant_required
def accountant_reports(request):
    today = timezone.localdate()
    current_year = today.year
    years = list(range(current_year, current_year - 5, -1))

    report_type = request.GET.get('report_type', '')
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', today.month))

    context = {
        'years': years,
        'report_type': report_type,
        'selected_year': selected_year,
        'selected_month': selected_month,
    }

    if report_type:
        data = _get_report_data(report_type, selected_year, selected_month, formatted=True)
        context.update(data)
    
    return render(request, 'accountant/reports.html', context)

import csv
from django.http import HttpResponse

@accountant_required
def accountant_reports_export(request):
    today = timezone.localdate()
    current_year = today.year
    
    report_type = request.GET.get('report_type', 'monthly')
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', today.month))

    data = _get_report_data(report_type, selected_year, selected_month, formatted=False)
    
    response = HttpResponse(content_type='text/csv')
    filename = f"{report_type}_report_{selected_year}_{selected_month}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    
    # Write Headers
    writer.writerow(data['report_headers'])
    
    # Write Data
    for row in data['report_data']:
        writer.writerow(row)
        
    # Write Totals
    if data.get('report_totals'):
        writer.writerow(data['report_totals'])
        
    return response

def _get_report_data(report_type, selected_year, selected_month, formatted=False):
    report_data = []
    report_headers = []
    report_totals = []
    report_title = ''
    summary = {}

    def fmt(val):
        if not formatted:
            return val
        return f'₹{val:,.0f}'

    if report_type == 'monthly':
        month_name = calendar.month_name[selected_month]
        report_title = f'Monthly Collection – {month_name} {selected_year}'
        report_headers = ['#', 'Date', 'Receipt #', 'Student', 'Mode', f'Amount{" (₹)" if formatted else ""}', 'Status']

        payments = FeePayment.objects.filter(
            payment_date__year=selected_year,
            payment_date__month=selected_month
        ).select_related('student', 'student__user').order_by('payment_date')

        total = Decimal('0')
        for i, p in enumerate(payments, 1):
            report_data.append([
                i,
                p.payment_date.strftime('%d %b %Y'),
                p.receipt_no,
                p.student.user.get_full_name(),
                p.get_payment_mode_display(),
                fmt(p.amount_paid),
                p.get_status_display(),
            ])
            total += p.amount_paid

        report_totals = ['', '', '', '', 'Total:', fmt(total), '']
        summary = {
            'total_collected': total,
            'total_transactions': len(report_data),
            'avg_payment': (total / len(report_data)) if report_data else 0,
        }

    elif report_type == 'annual':
        report_title = f'Annual Financial Summary – {selected_year}'
        report_headers = ['Month', 'Transactions', f'Collected{" (₹)" if formatted else ""}', f'Pending{" (₹)" if formatted else ""}']

        grand_collected = Decimal('0')
        grand_pending = Decimal('0')
        total_txns = 0

        for m in range(1, 13):
            collected = FeePayment.objects.filter(
                payment_date__year=selected_year, payment_date__month=m, status='PAID'
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            pending = FeePayment.objects.filter(
                payment_date__year=selected_year, payment_date__month=m, status='PENDING'
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            txns = FeePayment.objects.filter(
                payment_date__year=selected_year, payment_date__month=m
            ).count()

            report_data.append([
                calendar.month_name[m],
                txns,
                fmt(collected),
                fmt(pending),
            ])
            grand_collected += Decimal(str(collected))
            grand_pending += Decimal(str(pending))
            total_txns += txns

        report_totals = ['Total', total_txns, fmt(grand_collected), fmt(grand_pending)]
        summary = {
            'total_collected': grand_collected,
            'total_transactions': total_txns,
            'avg_payment': (grand_collected / total_txns) if total_txns else 0,
        }

    elif report_type == 'department':
        report_title = f'Department-wise Collection – {selected_year}'
        report_headers = ['Department', 'Students', f'Collected{" (₹)" if formatted else ""}', f'Pending{" (₹)" if formatted else ""}']

        from departments.models import Department
        departments = Department.objects.all()
        grand_collected = Decimal('0')
        grand_pending = Decimal('0')
        total_students = 0

        for dept in departments:
            dept_students = Student.objects.filter(department=dept)
            collected = FeePayment.objects.filter(
                student__department=dept, status='PAID',
                payment_date__year=selected_year
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            pending = FeePayment.objects.filter(
                student__department=dept, status='PENDING',
                payment_date__year=selected_year
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            student_count = dept_students.count()
            report_data.append([
                dept.name,
                student_count,
                fmt(collected),
                fmt(pending),
            ])
            grand_collected += Decimal(str(collected))
            grand_pending += Decimal(str(pending))
            total_students += student_count

        report_totals = ['Total', total_students, fmt(grand_collected), fmt(grand_pending)]
        summary = {
            'total_collected': grand_collected,
            'total_transactions': total_students,
            'avg_payment': (grand_collected / total_students) if total_students else 0,
        }
        
    return {
        'report_data': report_data,
        'report_headers': report_headers,
        'report_totals': report_totals,
        'report_title': report_title,
        'summary': summary,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  5. NOTICES
# ═══════════════════════════════════════════════════════════════════════════
@accountant_required
def accountant_notices(request):
    notices = Notice.objects.filter(
        Q(target_audience='ALL') | Q(posted_by=request.user)
    ).distinct().order_by('-created_at')
    return render(request, 'accountant/notices.html', {'notices': notices})


@accountant_required
def accountant_post_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        target_audience = request.POST.get('target_audience', 'ALL')
        attachment = request.FILES.get('attachment')

        notice = Notice(
            title=title,
            description=description,
            target_audience=target_audience,
            posted_by=request.user,
        )
        if attachment:
            notice.attachment = attachment
        notice.save()

        messages.success(request, 'Notice posted successfully.')
        return redirect('accountant_notices')

    return render(request, 'accountant/post_notice.html')

@accountant_required
def download_receipt_admin(request, payment_id):
    """
    Generate Fee Receipt PDF for Admin/Accountant.
    Reuses the student receipt template.
    """
    payment = get_object_or_404(FeePayment, id=payment_id)
    student = payment.student

    context = {
        'payment': payment,
        'student': student,
        'generated_at': timezone.now(),
        'is_admin_copy': True,
    }
    
    pdf = render_to_pdf('student/receipt_pdf.html', context)
    if pdf:
        filename = f"Receipt_{payment.receipt_no}.pdf"
        content = f"inline; filename={filename}"
        pdf['Content-Disposition'] = content
        return pdf
    return HttpResponse("Error Generating Receipt PDF", status=500)


# ═══════════════════════════════════════════════════════════════════════════
#  6. PROFILE
# ═══════════════════════════════════════════════════════════════════════════
@accountant_required
def accountant_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accountant_profile')

    return render(request, 'accountant/profile.html')
