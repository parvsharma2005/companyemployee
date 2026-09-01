from rest_framework import serializers
from .models import (
    EmployeeLeaveBalance,
    LeaveRequest
)
from .enums import (
    LeaveTypeEnum,
    LeaveRequestStatusEnum
)


class EmployeeLeaveBalanceSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    available_days = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        read_only=True
    )

    leave_type = serializers.ChoiceField(
        choices=LeaveTypeEnum.choices()
    )

    class Meta:
        model = EmployeeLeaveBalance

        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "year",
            "allocated_days",
            "used_days",
            "available_days",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "available_days",
        ]


class LeaveRequestSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    # leave_type = serializers.ChoiceField(
    #     choices=LeaveTypeEnum.choices()
    # )

    class Meta:
        model = LeaveRequest

        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
            "approved_by",
            "approved_at",
            "rejected_by",
            "rejected_at",
            "manager_comment",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "status",
            "approved_by",
            "approved_at",
            "rejected_by",
            "rejected_at",
            "manager_comment",
            "created_at",
            "updated_at"
        ]

    def validate(self, data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:

            if end_date < start_date:
                raise serializers.ValidationError(
                    {
                        "end_date": (
                            "End date must be greater than "
                            "or equal to start date."
                        )
                    }
                )

        return data