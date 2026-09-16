from django.db import models
import uuid

from employee.models import Employee


class PerformanceReview(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="performance_reviews"
    )

    reviewer = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_reviews"
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2
    )

    comments = models.TextField(
        blank=True
    )

    review_date = models.DateField()

    period = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class Award(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="awards"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    awarded_date = models.DateField()

    awarded_by = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.title