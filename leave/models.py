from django.db import models
import uuid

from employee.models import Employee
from .enums import LeaveRequestStatusEnum, LeaveTypeEnum


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

    leave_type = models.CharField(
        max_length=30,
        choices=LeaveTypeEnum.choices()
    )

    year = models.PositiveIntegerField()

    allocated_days = models.DecimalField(
        max_digits=12,
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
            f"{self.leave_type} - "
            f"{self.year}"
        )


class LeaveRequest(models.Model):
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

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

    leave_type = models.CharField(
        max_length=30,
        choices=LeaveTypeEnum.choices(),
        null=True,
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=LeaveRequestStatusEnum.choices(),
        default=LeaveRequestStatusEnum.PENDING.value
    )
    approved_by = models.ForeignKey(
    "employee.Employee",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="approved_leave_requests"
)

    approved_at = models.DateTimeField(
        auto_now=True
)

    rejected_by = models.ForeignKey(
    "employee.Employee",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="rejected_leave_requests"
)

    rejected_at = models.DateTimeField(
        auto_now=True
)

    manager_comment = models.TextField(
    blank=True,
    null=True
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
            f"{self.leave_type}"
        )