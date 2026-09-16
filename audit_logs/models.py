from django.db import models

# Create your models here.
import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("APPROVE", "Approve"),
        ("REJECT", "Reject"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    module = models.CharField(
        max_length=100
    )

    object_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    old_data = models.JSONField(
        null=True,
        blank=True
    )

    new_data = models.JSONField(
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.module}"