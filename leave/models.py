from django.db import models
import uuid

from employee.models import Employee


class LeaveType(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    total_days = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class EmployeeLeaveBalance(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_balances"
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name="employee_balances"
    )

    year = models.PositiveIntegerField()

    allocated_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    used_days = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    @property
    def available_days(self):
        return self.allocated_days - self.used_days

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "leave_type",
                    "year"
                ],
                name="unique_employee_leave_balance_per_year"
            )
        ]

    def __str__(self):
        return (
            f"{self.employee.name} - "
            f"{self.leave_type.name} - "
            f"{self.year}"
        )


class LeaveRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_requests"
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name="requests"
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.employee.name} - "
            f"{self.leave_type.name}"
        )