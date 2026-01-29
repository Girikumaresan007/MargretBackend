from django.db import models
class Client(models.Model):
    name = models.CharField(max_length=100)
    eventDate = models.DateField()
    email = models.EmailField(unique=True)
    message = models.TextField()

    class Meta:
        db_table = 'Client'

