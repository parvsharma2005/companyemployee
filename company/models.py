from django.db import models
import uuid

class company(models.Model):
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
    established = models.DateTimeField(auto_now=True)
    
    