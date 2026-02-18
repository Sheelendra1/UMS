from django.conf import settings
from django.db import models

class Attendance(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date = models.DateField()
    marked_by = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('course', 'date')

class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  # True = Present, False = Absent

    def __str__(self):
        return f"{self.student.enrollment_no} - {self.attendance.date}"
