from django.conf import settings
from django.db import models

class Timetable(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    faculty = models.ForeignKey('faculty.Faculty', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course.name} - {self.day_of_week}"
