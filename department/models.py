from django.db import models

# Create your models here.
from django.db import models
from company.models import Company
import uuid


class Department(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name