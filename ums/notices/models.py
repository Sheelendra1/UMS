from django.db import models
from django.conf import settings

class Notice(models.Model):
    AUDIENCE_CHOICES = (
        ('ALL', 'All'),
        ('FACULTY', 'Teachers'),
        ('STUDENT', 'Students'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='ALL')
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
