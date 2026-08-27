from rest_framework import serializers

from .models import (
    LeaveType,
    EmployeeLeaveBalance,
    LeaveRequest
)


class LeaveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveType
        fields = [
            "id",
            "name",
            "description",
            "total_days",
            "is_active",
        ]

        read_only_fields = [
            "id",
        ]


class EmployeeLeaveBalanceSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    leave_type_name = serializers.CharField(
        source="leave_type.name",
        read_only=True
    )

    available_days = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = EmployeeLeaveBalance

        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "leave_type_name",
            "year",
            "allocated_days",
            "used_days",
            "available_days",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "leave_type_name",
            "available_days",
        ]


class LeaveRequestSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    leave_type_name = serializers.CharField(
        source="leave_type.name",
        read_only=True
    )

    class Meta:
        model = LeaveRequest

        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "leave_type_name",
            "start_date",
            "end_date",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "leave_type_name",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError(
                    "End date must be greater than or equal to start date."
                )

        return data