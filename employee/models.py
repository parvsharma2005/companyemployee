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

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees"
    )

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
