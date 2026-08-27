from rest_framework import serializers

from .models import EmployeeHistoryLog


class EmployeeHistoryLogSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    class Meta:
        model = EmployeeHistoryLog

        fields = [
            "id",
            "employee",
            "employee_name",
            "action",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "created_at",
        ]