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

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.student.enrollment_no} - {self.amount_paid}"
