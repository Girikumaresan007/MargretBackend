from django.db import models

class Book(models.Model):
    package_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_location = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    attendees = models.PositiveIntegerField()
    requirements = models.TextField(blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100, blank=True)
    agree_terms = models.BooleanField(default=False)
    class Meta:
        db_table = "Book"


