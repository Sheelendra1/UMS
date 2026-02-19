from django.conf import settings
from django.db import models

class Exam(models.Model):
    class ExamType(models.TextChoices):
        MID = "MID", "Mid Term"
        FINAL = "FINAL", "Final Term"
        INTERNAL = "INTERNAL", "Internal"

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    total_marks = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    room_number = models.CharField(max_length=50, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.name} - {self.exam_type}"

class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.enrollment_no} - {self.exam}"
