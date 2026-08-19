from django.db import models
from company.models import Company
from department.models import Department
import uuid


class Employee(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=10
    )

    address = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employees"
    )

    def __str__(self):
        return self.name