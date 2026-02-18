from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    hod = models.ForeignKey(
        'faculty.Faculty', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hod_department'
    )

    def __str__(self):
        return f"{self.name} ({self.code})"
