from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import InvestmentDeclaration
from .serializers import InvestmentDeclarationSerializer


class InvestmentDeclarationViewSet(viewsets.ModelViewSet):

    queryset = InvestmentDeclaration.objects.select_related(
        "employee"
    ).all()

    serializer_class = InvestmentDeclarationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        financial_year = self.request.query_params.get(
            "financial_year"
        )

        status = self.request.query_params.get(
            "status"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if financial_year:
            queryset = queryset.filter(
                financial_year=financial_year
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset