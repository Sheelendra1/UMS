import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ums.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME = 'admin'
EMAIL = 'admin@example.com'
PASSWORD = 'adminpassword'

if not User.objects.filter(username=USERNAME).exists():
    t = User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f'Superuser "{USERNAME}" created successfully.')
else:
    print(f'Superuser "{USERNAME}" already exists.')
