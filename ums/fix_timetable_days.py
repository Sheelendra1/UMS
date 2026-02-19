import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ums.settings')
django.setup()

from timetable.models import Timetable

DAY_MAP = {
    '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday',
    '4': 'Thursday', '5': 'Friday', '6': 'Saturday', '7': 'Sunday',
    '8': 'Monday', # Just in case
}

count = 0
for t in Timetable.objects.all():
    original = t.day_of_week
    if original in DAY_MAP:
        t.day_of_week = DAY_MAP[original]
        t.save()
        count += 1
        print(f"Updated {t} from {original} to {t.day_of_week}")
    elif original.capitalize() in DAY_MAP.values():
        # normalize capitalization
        pass # already good if capitalized correctly? No, store capitalized.
        
print(f"Fixed {count} Timetable entries.")
