from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from employee.models import Employee
from attendance.models import Attendance
from notification.models import Notification
from leave.models import EmployeeLeaveBalance, LeaveRequest


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            employee = Employee.objects.get(user=request.user)

            notifications = Notification.objects.filter(
                recipient=request.user
            )
            attendance = Attendance.objects.filter(
    employee=employee
)
            leave_balances = EmployeeLeaveBalance.objects.filter(
    employee=employee
)

            leave_requests = LeaveRequest.objects.filter(
    employee=employee
)

            return Response(
                {
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
    "holiday": attendance.filter(
        status="holiday"
    ).count(),
},
                    "leave": {
    "balances": [
        {
            "leave_type": balance.leave_type,
            "year": balance.year,
            "allocated_days": balance.allocated_days,
            "used_days": balance.used_days,
            "available_days": balance.available_days,
        }
        for balance in leave_balances
    ],

    "requests": {
        "total": leave_requests.count(),
        "pending": leave_requests.filter(
            status="pending"
        ).count(),
        "approved": leave_requests.filter(
            status="approved"
        ).count(),
        "rejected": leave_requests.filter(
            status="rejected"
        ).count(),
    },
},

                    "notifications": {
                        "total": notifications.count(),
                        "unread": notifications.filter(
                            is_read=False
                        ).count(),
                    },
                },
                status=status.HTTP_200_OK
            )

        except Employee.DoesNotExist:
            return Response(
                {
                    "detail": "Employee profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )