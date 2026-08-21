from django.db import models
from company.models import *
import uuid
# needmsndsm

class Employee(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    name = models.CharField(max_length=200)

    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.TextField(blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
    
