from django.db import models
import uuid

from company.models import Company
from department.models import Department


class JobOpening(models.Model):

    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("on_hold", "On Hold"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="job_openings"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="job_openings"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    vacancies = models.PositiveIntegerField(
        default=1
    )

    location = models.CharField(
        max_length=200
    )

    opening_date = models.DateField()

    closing_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title