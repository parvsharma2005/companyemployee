from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from employee.models import Employee
from attendance.models import Attendance
from leave.models import EmployeeLeaveBalance, LeaveRequest
from notification.models import Notification

from .serializers import DashboardSerializer


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            employee = Employee.objects.get(user=request.user)

            attendance = Attendance.objects.filter(
                employee=employee
            )

            leave_balance = EmployeeLeaveBalance.objects.filter(
                employee=employee
            )

            leave_requests = LeaveRequest.objects.filter(
                employee=employee
            )

            notifications = Notification.objects.filter(
                employee=employee
            )

            data = {
                "employee": {
                    "id": str(employee.id),
                    "name": employee.name,
                    "email": employee.email,
                    "phone": employee.phone,
                    "department": (
                        employee.department.name
                        if employee.department
                        else None
                    ),
                },

                "attendance": {
                    "total": attendance.count(),
                    "present": attendance.filter(
                        status="present"
                    ).count(),
                    "absent": attendance.filter(
                        status="absent"
                    ).count(),
                    "leave": attendance.filter(
                        status="leave"
                    ).count(),
                    "weekly_off": attendance.filter(
                        status="weekly_off"
                    ).count(),
                },

                "leave": {
                    "total_leave_balances": leave_balance.count(),
                    "total_requests": leave_requests.count(),
                    "pending_requests": leave_requests.filter(
                        status="pending"
                    ).count(),
                    "approved_requests": leave_requests.filter(
                        status="approved"
                    ).count(),
                    "rejected_requests": leave_requests.filter(
                        status="rejected"
                    ).count(),
                },

                "notifications": {
                    "total": notifications.count(),
                    "unread": notifications.filter(
                        is_read=False
                    ).count(),
                },
            }

            serializer = DashboardSerializer(data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Employee.DoesNotExist:
            return Response(
                {
                    "detail": "Employee profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )