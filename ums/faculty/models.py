from django.conf import settings
from django.db import models

class Faculty(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.designation}"
