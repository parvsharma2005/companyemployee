from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    LeaveType,
    EmployeeLeaveBalance,
    LeaveRequest
)

from .serializers import (
    LeaveTypeSerializer,
    EmployeeLeaveBalanceSerializer,
    LeaveRequestSerializer
)


class LeaveTypeViewSet(viewsets.ModelViewSet):

    queryset = LeaveType.objects.all()

    serializer_class = LeaveTypeSerializer

    permission_classes = [
        IsAuthenticated
    ]


class EmployeeLeaveBalanceViewSet(viewsets.ModelViewSet):

    queryset = EmployeeLeaveBalance.objects.select_related(
        "employee",
        "leave_type"
    ).all()

    serializer_class = EmployeeLeaveBalanceSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        year = self.request.query_params.get(
            "year"
        )

        leave_type_id = self.request.query_params.get(
            "leave_type"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if year:
            queryset = queryset.filter(
                year=year
            )

        if leave_type_id:
            queryset = queryset.filter(
                leave_type_id=leave_type_id
            )

        return queryset


class LeaveRequestViewSet(viewsets.ModelViewSet):

    queryset = LeaveRequest.objects.select_related(
        "employee",
        "leave_type"
    ).all()

    serializer_class = LeaveRequestSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        status = self.request.query_params.get(
            "status"
        )

        leave_type_id = self.request.query_params.get(
            "leave_type"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if leave_type_id:
            queryset = queryset.filter(
                leave_type_id=leave_type_id
            )

        return queryset