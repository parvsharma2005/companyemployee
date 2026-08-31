from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    EmployeeLeaveBalance,
    LeaveRequest
)

from .serializers import (
    EmployeeLeaveBalanceSerializer,
    LeaveRequestSerializer
)

class EmployeeLeaveBalanceViewSet(viewsets.ModelViewSet):

    queryset = EmployeeLeaveBalance.objects.select_related(
        "employee"
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

        if leave_type:
            queryset = queryset.filter(
                leave_type=leave_type
            )

        return queryset


class LeaveRequestViewSet(viewsets.ModelViewSet):

    queryset = LeaveRequest.objects.select_related(
        "employee"
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

        leave_type = self.request.query_params.get(
            "leave_type"
        )

        status_filter = self.request.query_params.get(
            "status"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if leave_type:
            queryset = queryset.filter(
                leave_type=leave_type
            )

        if status_filter:
            queryset = queryset.filter(
                status=status_filter
            )

        return queryset

    # your get_queryset() here

    @action(
        detail=True,
        methods=["patch"],
        url_path="approve"
    )
    def approve(self, request, pk=None):

        leave_request = self.get_object()

        if leave_request.status != "pending":
            return Response(
                {
                    "error": "Only pending leave requests can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_request.status = "approved"
        leave_request.save()

        return Response(
            {
                "message": "Leave approved successfully.",
                "status": leave_request.status
            },
            status=status.HTTP_200_OK
        )
        
         # ADD REJECT HERE

    @action(
        detail=True,
        methods=["patch"],
        url_path="reject"
    )
    def reject(self, request, pk=None):

        leave_request = self.get_object()

        if leave_request.status != "pending":
            return Response(
                {
                    "error": "Only pending leave requests can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_request.status = "rejected"
        leave_request.save()

        return Response(
            {
                "message": "Leave rejected successfully.",
                "status": leave_request.status
            },
            status=status.HTTP_200_OK
        )