from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ImprestRequest
from .serializers import ImprestRequestSerializer


class ImprestRequestViewSet(viewsets.ModelViewSet):

    queryset = ImprestRequest.objects.select_related(
        "employee"
    ).all()

    serializer_class = ImprestRequestSerializer

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

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset