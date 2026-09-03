from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):

    queryset = Attendance.objects.select_related("employee").all()

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get("employee")
        status = self.request.query_params.get("status")
        date = self.request.query_params.get("date")

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if date:
            queryset = queryset.filter(
                date=date
            )

        return queryset