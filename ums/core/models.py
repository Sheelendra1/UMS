from django.db import models

class UniversitySetting(models.Model):
    university_name = models.CharField(max_length=200, default="My University")
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    academic_year = models.CharField(max_length=20, default="2024-2025")
    current_semester = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk and UniversitySetting.objects.exists():
            # Enforce singleton behavior
            self.pk = UniversitySetting.objects.first().pk
        super(UniversitySetting, self).save(*args, **kwargs)

    def __str__(self):
        return "University Configuration"
