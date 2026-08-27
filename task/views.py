from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.select_related(
        "employee"
    ).all()

    serializer_class = TaskSerializer

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

        priority = self.request.query_params.get(
            "priority"
        )

        search = self.request.query_params.get(
            "search"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if priority:
            queryset = queryset.filter(
                priority=priority
            )

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        return queryset