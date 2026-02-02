from django.db import models
from django.contrib.auth.models import User
import uuid

class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "password_reset_tokens"
        ordering = ["-created_at"]


# Create your models here.

