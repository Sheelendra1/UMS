from django import forms
from django.db.models import Q
from .models import Timetable

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'faculty', 'day_of_week', 'start_time', 'end_time', 'room_number']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day_of_week')
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        faculty = cleaned_data.get('faculty')
        room = cleaned_data.get('room_number')
        course = cleaned_data.get('course')

        if not (day and start and end and faculty and room):
            return cleaned_data

        if start >= end:
            self.add_error('end_time', "End time must be after start time.")

        # Check for overlaps
        # Overlap condition: existing.start < new.end AND existing.end > new.start
        
        # Base query: same day, time overlap
        overlap_query = Timetable.objects.filter(
            day_of_week=day,
            start_time__lt=end,
            end_time__gt=start
        )

        if self.instance.pk:
            overlap_query = overlap_query.exclude(pk=self.instance.pk)

        # check faculty availability
        if overlap_query.filter(faculty=faculty).exists():
            self.add_error('faculty', f"Faculty {faculty} is already busy at this time.")

        # check room availability
        if overlap_query.filter(room_number=room).exists():
            self.add_error('room_number', f"Room {room} is already booked at this time.")
        
        # check course availability (students can't be in two places)
        # Assuming one course = one batch of students. 
        # Ideally check if students of this course are busy, but course-level check is a good proxy.
        if overlap_query.filter(course=course).exists():
             self.add_error('course', f"Course {course} already has a class at this time.")

        return cleaned_data
