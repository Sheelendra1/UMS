from django.conf import settings
from django.db import models

class FeeStructure(models.Model):
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    semester = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.department.name} - Sem {self.semester}"

class FeePayment(models.Model):
    class Status(models.TextChoices):
        PAID = "PAID", "Paid"
        PENDING = "PENDING", "Pending"

    class PaymentMode(models.TextChoices):
        CASH = "CASH", "Cash"
        CHEQUE = "CHEQUE", "Cheque"
        ONLINE = "ONLINE", "Online"

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_mode = models.CharField(max_length=20, choices=PaymentMode.choices, default=PaymentMode.CASH)
    receipt_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='collected_payments'
    )

    def save(self, *args, **kwargs):
        if not self.receipt_no:
            import uuid
            self.receipt_no = f"RCP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.enrollment_no} - {self.amount_paid}"
