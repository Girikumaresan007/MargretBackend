from django.db import models

class Book(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_date = models.DateField()
    event_type = models.CharField(max_length=100)
    event_location = models.CharField(max_length=255)
    package_name = models.CharField(max_length=100)
    attendees = models.IntegerField()
    requirements = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True)
    agree_terms = models.BooleanField(default=False)

    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "book"   # ✅ MUST be lowercase
