from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from audit_logs.utils import create_audit_log

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

        if leave_type_id:
            queryset = queryset.filter(
                leave_type_id=leave_type_id
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
        return LeaveRequest.objects.filter(
            employee__user=self.request.user
        )

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

        # Logged-in Employee
        manager = request.user.employee

        # -------------------------------------------------
        # Check whether logged-in employee is the manager
        # -------------------------------------------------

        if leave_request.employee.manager_id != manager.id:

            return Response(
                {
                    "detail":
                    "You are not the manager of this employee."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if leave_request.status != "pending":

            return Response(
                {
                    "detail":
                    "Only pending leave requests can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_request.status = "approved"
        leave_request.approved_by = manager
        leave_request.approved_at = timezone.now()

        leave_request.save()
        create_audit_log(
    user=request.user,
    action="APPROVE",
    module="Leave",
    object_id=leave_request.id,
    description="Manager approved the leave request",
    new_data={
        "status": leave_request.status,
        "approved_by": str(manager.id),
        "approved_at": str(leave_request.approved_at),
    },
    ip_address=request.META.get("REMOTE_ADDR"),
)

        serializer = self.get_serializer(
            leave_request
        )

        return Response(
            serializer.data,
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

        manager = request.user.employee

        if leave_request.employee.manager_id != manager.id:

            return Response(
                {
                    "detail":
                    "You are not the manager of this employee."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if leave_request.status != "pending":

            return Response(
                {
                    "detail":
                    "This leave request has already been processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_request.status = "rejected"
        leave_request.rejected_by = manager
        leave_request.rejected_at = timezone.now()

        leave_request.save()
        create_audit_log(
    user=request.user,
    action="REJECT",
    module="Leave",
    object_id=leave_request.id,
    description="Manager rejected the leave request",
    new_data={
        "status": leave_request.status,
        "rejected_by": str(manager.id),
        "rejected_at": str(leave_request.rejected_at),
    },
    ip_address=request.META.get("REMOTE_ADDR"),
)

        serializer = self.get_serializer(
            leave_request
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class LeaveRequestApproveView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            leave_request = LeaveRequest.objects.get(pk=pk)

        except LeaveRequest.DoesNotExist:

            return Response(
                {"detail": "Leave request not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        manager = request.user.employee

        # Check that this employee's manager
        # is the logged-in user

        if leave_request.employee.manager_id != manager.id:

            return Response(
                {
                    "detail":
                    "You are not the manager of this employee."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if leave_request.status != "pending":

            return Response(
                {
                    "detail":
                    "Only pending leave requests can be approved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_request.status = "approved"
        leave_request.approved_by = manager
        leave_request.approved_at = timezone.now()

        leave_request.manager_comment = request.data.get(
            "manager_comment",
            ""
        )

        leave_request.save()
        create_audit_log(
    user=request.user,
    action="APPROVE",
    module="Leave",
    object_id=leave_request.id,
    description="Manager approved the leave request",
    new_data={
        "status": leave_request.status,
        "approved_by": str(manager.id),
        "approved_at": str(leave_request.approved_at),
        "manager_comment": leave_request.manager_comment,
    },
    ip_address=request.META.get("REMOTE_ADDR"),
)

        return Response(
            {
                "message":
                "Leave request approved successfully.",

                "leave_request_id":
                leave_request.id,

                "status":
                leave_request.status,

                "approved_by":
                manager.id,

                "approved_at":
                leave_request.approved_at,

                "manager_comment":
                leave_request.manager_comment,
            },
            status=status.HTTP_200_OK
        )


class LeaveRequestRejectView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            leave_request = LeaveRequest.objects.get(pk=pk)

        except LeaveRequest.DoesNotExist:

            return Response(
                {"detail": "Leave request not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        manager = request.user.employee

        if leave_request.employee.manager_id != manager.id:

            return Response(
                {
                    "detail":
                    "You are not the manager of this employee."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if leave_request.status != "pending":

            return Response(
                {
                    "detail":
                    "Only pending leave requests can be rejected."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        leave_request.status = "rejected"
        leave_request.rejected_by = manager
        leave_request.rejected_at = timezone.now()

        leave_request.manager_comment = request.data.get(
            "manager_comment",
            ""
        )

        leave_request.save()
        create_audit_log(
            user=request.user,
            action="REJECT",
            module="Leave",
            object_id="leave_request.id",
            description="Manager rejected the leave request",
    new_data={
        "status": leave_request.status,
        "rejected_by": str(manager.id),
        "rejected_at": str(leave_request.rejected_at),
        "manager_comment": leave_request.manager_comment,
    },
    ip_address=request.META.get("REMOTE_ADDR"),
        )

        return Response(
            {
                "message":
                "Leave request rejected successfully.",

                "leave_request_id":
                leave_request.id,

                "status":
                leave_request.status,

                "rejected_by":
                manager.id,

                "rejected_at":
                leave_request.rejected_at,

                "manager_comment":
                leave_request.manager_comment,
            },
            status=status.HTTP_200_OK
        )


class ManagerLeaveRequestListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        manager = request.user.employee

        leave_requests = LeaveRequest.objects.filter(
            employee__manager=manager
        ).order_by("-created_at")

        serializer = LeaveRequestSerializer(
            leave_requests,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )