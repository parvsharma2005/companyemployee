from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import EmployeeHistoryLog
from .serializers import EmployeeHistoryLogSerializer


class EmployeeHistoryLogViewSet(viewsets.ModelViewSet):

    queryset = EmployeeHistoryLog.objects.select_related(
        "employee"
    ).all()

    serializer_class = EmployeeHistoryLogSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        action = self.request.query_params.get(
            "action"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if action:
            queryset = queryset.filter(
                action__icontains=action
            )

        return queryset