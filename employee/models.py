from django.db import models
from department.models import Department
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
class EmployeeAccount(
    AbstractBaseUser,
    PermissionsMixin
):
    ROLE_CHOICES = (
        ("employee", "Employee"),
        ("manager", "Manager"),
        ("hr", "HR"),
        ("admin", "Admin"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    phone = models.CharField(
        max_length=10,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="employee"
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.phone

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    phone = models.CharField(
        max_length=10,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.phone

class Employee(models.Model):
        
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )

    user = models.OneToOneField(
        EmployeeAccount,
        on_delete=models.CASCADE,
        related_name="employee",
    )
    
    manager = models.ForeignKey(
    "self",
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name="team_members"
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
    profile_picture = models.ImageField(
        upload_to="employee/employees/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    
class EmployeeAddress(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    address_type = models.CharField(
        max_length=50
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    pincode = models.CharField(
        max_length=10
    )

    def __str__(self):
        return f"{self.employee.name} - {self.address_type}"
    
class EmployeeEducation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="education"
    )

    qualification = models.CharField(
        max_length=150
    )

    institution = models.CharField(
        max_length=200
    )

    specialization = models.CharField(
        max_length=150,
        blank=True
    )

    start_year = models.PositiveIntegerField()

    end_year = models.PositiveIntegerField()

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.qualification}"
    
class EmployeeExperience(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="experiences"
    )

    company_name = models.CharField(
        max_length=200
    )

    designation = models.CharField(
        max_length=150
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.company_name}"
    
class EmergencyContact(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="emergency_contacts"
    )

    name = models.CharField(
        max_length=150
    )

    relationship = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.name}"