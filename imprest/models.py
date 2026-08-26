from django.db import models
import uuid

from employee.models import Employee


class ImprestRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("settled", "Settled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="imprest_requests"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    purpose = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.amount}"