from django.db import models
import uuid

class Company(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    name = models.CharField(max_length=201)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    website = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    established = models.DateField()
    
    def __str__(self):
        return self.name