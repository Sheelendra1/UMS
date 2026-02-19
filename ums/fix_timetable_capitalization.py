import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ums.settings')
django.setup()

from timetable.models import Timetable

DAY_MAP = {
    '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday',
    '4': 'Thursday', '5': 'Friday', '6': 'Saturday', '7': 'Sunday',
}

count = 0
for t in Timetable.objects.all():
    original = t.day_of_week
    # If numeric
    if original in DAY_MAP:
        t.day_of_week = DAY_MAP[original]
        t.save()
        count += 1
        print(f"Updated {original} -> {t.day_of_week}")
    else:
        # Check casing
        capitalized = original.capitalize()
        # Ensure it is a valid day name
        if capitalized in DAY_MAP.values():
             if original != capitalized:
                 t.day_of_week = capitalized
                 t.save()
                 count += 1
                 print(f"Capitalized {original} -> {t.day_of_week}")
        # Else: invalid day string?
        
print(f"Fixed {count} additional entries.")
