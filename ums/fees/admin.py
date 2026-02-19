from django.contrib import admin
from .models import FeeStructure, FeePayment


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('department', 'semester', 'amount')
    list_filter = ('department', 'semester')


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'payment_date', 'status', 'payment_mode', 'receipt_no', 'collected_by')
    list_filter = ('status', 'payment_mode', 'payment_date')
    search_fields = ('student__enrollment_no', 'receipt_no')
    raw_id_fields = ('student', 'collected_by')
