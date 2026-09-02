from django.db import models
import uuid
# Create your models here.
from django.db import models
from employee.models import EmployeeAccount


class Notification(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    recipient = models.ForeignKey(
        EmployeeAccount,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def create_notification(recipient, title, message, notification_type):
        Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type
    )