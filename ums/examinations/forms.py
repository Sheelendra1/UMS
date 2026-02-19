from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'exam_type', 'total_marks', 'date', 'start_time', 'end_time', 'room_number', 'is_published']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'exam_type': forms.Select(attrs={'class': 'form-select'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
