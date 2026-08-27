from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):

    queryset = Expense.objects.select_related(
        "employee"
    ).all()

    serializer_class = ExpenseSerializer

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        status = self.request.query_params.get(
            "status"
        )

        category = self.request.query_params.get(
            "category"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if category:
            queryset = queryset.filter(
                category__icontains=category
            )

        return queryset