from django.contrib import admin
from .models import FeeStructure, FeePayment

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('department', 'semester', 'amount')
    list_filter = ('department', 'semester')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'payment_date', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('student__enrollment_no',)
