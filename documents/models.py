from django.db import models
import uuid

from employee.models import Employee


class EmployeeDocument(models.Model):

    DOCUMENT_TYPES = [
        ("identity", "Identity"),
        ("employee_letter", "Employee Letter"),
        ("previous_experience", "Previous Experience"),
        ("degree_certificate", "Degree / Certificate"),
        ("other", "Other"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES
    )

    document_name = models.CharField(
        max_length=200
    )

    file = models.FileField(
        upload_to="employee_documents/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.document_name}"