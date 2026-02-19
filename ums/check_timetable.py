import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ums.settings')
django.setup()

from timetable.models import Timetable
from courses.models import Course
from faculty.models import Faculty
from students.models import Student

print(f"Total Timetable entries: {Timetable.objects.count()}")
for t in Timetable.objects.all():
    print(f"Entry: {t.course.name} - {t.day_of_week} {t.start_time}-{t.end_time} ({t.faculty.user.username})")

print(f"\nTotal Courses: {Course.objects.count()}")
print(f"Total Faculty: {Faculty.objects.count()}")

# Check sample student enrollment
first_student = Student.objects.first()
if first_student:
    print(f"\nFirst Student: {first_student.user.username}")
    print(f"Enrolled Courses: {[c.name for c in first_student.enrolled_courses.all()]}")
    
    # Check timetable for these courses
    entries = Timetable.objects.filter(course__in=first_student.enrolled_courses.all())
    print(f"Applicable Timetable Entries: {entries.count()}")
else:
    print("\nNo students found.")
