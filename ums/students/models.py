from django.conf import settings
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True)
    semester = models.IntegerField()
    admission_date = models.DateField()

    def __str__(self):
        return f"{self.enrollment_no} - {self.user.username}"
