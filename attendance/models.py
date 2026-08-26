from django.db import models
import uuid

from employee.models import Employee


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("leave", "Leave"),
        ("weekly_off", "Weekly Off"),
        ("holiday", "Holiday"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date"],
                name="unique_employee_attendance_per_day"
            )
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"