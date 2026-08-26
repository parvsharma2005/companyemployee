from django.db import models
import uuid

from company.models import Company
from employee.models import Employee


class Asset(models.Model):

    STATUS_CHOICES = [
        ("available", "Available"),
        ("assigned", "Assigned"),
        ("maintenance", "Maintenance"),
        ("retired", "Retired"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="assets"
    )

    asset_name = models.CharField(
        max_length=200
    )

    asset_code = models.CharField(
        max_length=100,
        unique=True
    )

    category = models.CharField(
        max_length=100
    )

    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_assets"
    )

    assigned_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.asset_name} - {self.asset_code}"