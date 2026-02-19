from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    faculty = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True)
    semester = models.IntegerField()
    credits = models.IntegerField()
    capacity = models.IntegerField(default=60)
    students = models.ManyToManyField('students.Student', related_name='enrolled_courses', blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
